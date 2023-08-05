# Copyright 2011-2015 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABCMeta
from collections import MutableMapping, Mapping, namedtuple
import datetime
import fnmatch
import mimetypes
import netrc
import os
import re
import sys
import textwrap
import threading
import urllib
import urlparse

import isodate
import requests


# Some type conversion functions
def to_date(value):
    return isodate.parse_date(value)


def to_time(value):
    return isodate.parse_time(value)


def to_datetime(value):
    return isodate.parse_datetime(value)


def to_timedelta(value):
    return isodate.parse_duration(value).tdelta


def to_bool(value):
    return value in ["true", "1"]


def from_datetime(value):
    if isinstance(value, str):
        value = isodate.parse_datetime(str)

    if isinstance(value, datetime.datetime):
        return value.isoformat()
    else:
        raise ValueError('To create a proper string representation for a datetime, either a datetime.datetime or str has to be supplied!')


def from_date(value):
    if isinstance(value, str):
        value = isodate.parse_date(str)

    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        raise ValueError('To create a proper string representation for a date, either a datetime.date or str has to be supplied!')


def from_time(value):
    if isinstance(value, str):
        value = isodate.parse_time(str)

    if isinstance(value, datetime.time):
        return value.isoformat()
    else:
        raise ValueError('To create a proper string representation for a time, either a datetime.time or str has to be supplied!')


def from_timedelta(value):
    if isinstance(value, str):
        value = isodate.parse_duration(str)
    elif isinstance(value, datetime.timedelta):
        value = isodate.duration.Duration(days=value.days,
                                          seconds=value.seconds,
                                          microseconds=value.microseconds)

    if isinstance(value, isodate.duration.Duration):
        return isodate.duration_isoformat(value)
    else:
        raise ValueError('To create a proper string representation for a duration, either a isodate.duration.Duration or str has to be supplied!')


def from_bool(value):
    if isinstance(value, str):
        if value in ["true", "false", "1", "0"]:
            return value
        else:
            raise ValueError('Value {} is not a valid string representation of a bool'.format(value))
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    else:
        raise TypeError('To create a proper string presentation for a bool, either a bool or str has to be supplied!')


def from_int(value):
    if not isinstance(value, int):
        value = int(str)
    return str(value)


def from_float(value):
    if not isinstance(value, float):
        value = float(str)
    return str(value)


# Here to be after all needed function definitions
TYPE_TO_MAP = {
    'xs:anyURI': str,
    'xs:string': str,
    'xs:boolean': to_bool,
    'xs:integer': int,
    'xs:long': int,
    'xs:float': float,
    'xs:double': float,
    'xs:dateTime': to_datetime,
    'xs:time': to_time,
    'xs:date': to_date,
    'xs:duration': to_timedelta,
}

TYPE_FROM_MAP = {
    'xs:anyURI': str,
    'xs:string': str,
    'xs:boolean': from_bool,
    'xs:integer': from_int,
    'xs:long': from_int,
    'xs:float': from_float,
    'xs:double': from_float,
    'xs:dateTime': from_datetime,
    'xs:time': from_time,
    'xs:date': from_date,
    'xs:duration': from_timedelta,
}

def caching(func):
    """
    This decorator caches the value in self._cache to avoid data to be
    retrieved multiple times. This works for properties or functions without
    arguments.
    """
    name = func.func_name

    def wrapper(self):
        # We use self._cache here, in the decorator _cache will be a member of
        #  the objects, so nothing to worry about
        # pylint: disable=protected-access
        if not self.caching or name not in self._cache:
            # Compute the value if not cached
            self._cache[name] = func(self)

        return self._cache[name]

    docstring = func.__doc__ if func.__doc__ is not None else ''
    wrapper.__doc__ = textwrap.dedent(docstring) + '\nCached using the caching decorator'
    return wrapper


class XNATResponseError(ValueError):
    pass


class XNATIOError(IOError):
    pass


class XNATUploadError(XNATIOError):
    pass


class XNATSSLError(requests.exceptions.SSLError):
    pass


class VariableMap(MutableMapping):
    def __init__(self, parent, field):
        self._cache = {}
        self.caching = True
        self.parent = parent
        self._field = field

    def __repr__(self):
        return "<VariableMap {}>".format(dict(self))

    @property
    @caching
    def data(self):
        try:
            variables = next(x for x in self.parent.fulldata['children'] if x['field'] == self.field)
            variables_map = {x['data_fields']['name']: x['data_fields']['field'] for x in variables['items'] if 'field' in x['data_fields']}
        except StopIteration:
            variables_map = {}

        return variables_map

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        query = {'xsiType': self.parent.xsi_type,
                 '{parent_type_}/{field}[@xsi_type={type}]/{key}'.format(parent_type_=self.parent.xsi_type,
                                                                         field=self.field,
                                                                         type=self.xsi_type,
                                                                         key=key): value}
        self.xnat.put(self.parent.fulluri, query=query)

        # Remove cache and make sure the reload the data
        if 'data' in self._cache:
            self.clearcache()

    def __delitem__(self, key):
        print('[WARNING] Deleting of variables is currently not supported!')

    def __iter__(self):
        for key in self.data.keys():
            yield key

    def __len__(self):
        return len(self.data)

    @property
    def field(self):
        return self._field

    @property
    def xnat(self):
        return self.parent.xnat

    def clearcache(self):
        self._cache.clear()
        self.parent.clearcache()


class CustomVariableMap(VariableMap):
    def __setitem__(self, key, value):
        query = {'xsiType': self.parent.xsi_type,
                 '{type_}/fields/field[name={key}]/field'.format(type_=self.parent.xsi_type,
                                                                 key=key): value}
        self.xnat.put(self.parent.fulluri, query=query)

        # Remove cache and make sure the reload the data
        if 'data' in self._cache:
            self.clearcache()


class XNATObject(object):
    __metaclass__ = ABCMeta
    _HAS_FIELDS = False
    _XSI_TYPE = 'xnat:baseObject'

    def __init__(self, uri, xnat, id_=None, datafields=None, parent=None, fieldname=None):
        # Set the xnat session
        self._cache = {}
        self._caching = None

        self._xnat = xnat
        self._uri = uri
        self._parent = parent
        self._fieldname = fieldname

        if self._HAS_FIELDS:
            self._fields = CustomVariableMap(self, field='fields/field')
        else:
            self._fields = None

        if id_ is not None:
            self._cache['id'] = id_

        if datafields is not None:
            self._cache['data'] = datafields

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    @property
    def parent(self):
        return self._parent

    @property
    def fieldname(self):
        return self._fieldname

    def get(self, name, type_=None):
        value = self.data.get(name)
        if type_ is not None and value is not None:
            if isinstance(type_, str):
                value = TYPE_TO_MAP.get(type_, str)(value)
            else:
                value = type_(value)
        return value
    
    _TYPE_HINTS = {
            'demographics': 'xnat:demographicData',
            'investigator': 'xnat:investigatorData',
            'metadata': 'xnat:subjectMetadata',
            'pi': 'xnat:investigatorData',
            'studyprotocol': 'xnat:studyProtocol',
            'validation': 'xnat:validationData',
            'baseimage': 'xnat:abstractResource',
            }

    def get_object(self, fieldname):
        try:
            data = next(x for x in self.fulldata['children'] if x['field'] == fieldname)['items'][0]
            type_ = data['meta']['xsi:type']
        except StopIteration:
            type_ = self._TYPE_HINTS.get(fieldname)
        if type_ is None:
            raise ValueError('Cannot determine type of field {}!'.format(fieldname))
        return self.xnat.create_object(self.uri, type_=type_, parent=self, fieldname=fieldname)

    @property
    def fulluri(self):
        return self.uri

    def set(self, name, value, type_=None):
        if type_ is not None:
            if isinstance(type_, str):
                # Make sure we have a valid string here that is properly casted
                value = TYPE_FROM_MAP[type_](value)
            else:
                value = type_(value)

        if self.parent is None:
            query = {'xsiType': self.xsi_type,
                    '{xsitype}/{name}'.format(xsitype=self.xsi_type, name=name): value}
            self.xnat.put(self.fulluri, query=query)
            self.clearcache()
        else:
            query = {'xsiType': self.parent.xsi_type,
                     '{parent_type}/{fieldname}[@xsi:type={xsitype}]/{name}'.format(parent_type=self.parent.xsi_type,
                                                                                 fieldname=self.fieldname,
                                                                                 xsitype=self.xsi_type,
                                                                                 name=name): value}
            self.xnat.put(self.parent.fulluri, query=query)
            self.parent.clearcache()

    @property
    def xsi_type(self):
        return self._XSI_TYPE

    @property
    @caching
    def id(self):
        if 'ID' in self.data:
            return self.data['ID']
        elif self.parent is not None:
            return '{}/{}'.format(self.parent.id, self.fieldname)
        else:
            return '#NOID#'

    @property
    @caching
    def fulldata(self):
        return self.xnat.get_json(self.uri)['items'][0]

    @property
    def data(self):
        if self.parent is None:
            return self.fulldata['data_fields']
        else:
            try:
                data = next(x for x in self.parent.fulldata['children'] if x['field'] == self.fieldname)['items'][0]['data_fields']
            except StopIteration:
                data = {}
            return data

    @property
    def xnat(self):
        return self._xnat

    @property
    def uri(self):
        return self._uri

    def clearcache(self):
        self._cache.clear()

    # This needs to be at the end of the class because it shadows the caching
    # decorator for the remainder of the scope.
    @property
    def caching(self):
        if self._caching is not None:
            return self._caching
        else:
            return self.xnat.caching

    @caching.setter
    def caching(self, value):
        self._caching = value

    @caching.deleter
    def caching(self):
        self._caching = None

    def delete(self, remove_files=True):
        """
        Remove the item from XNAT
        """
        query = {}

        if remove_files:
            query['removeFiles'] = 'true'

        self.xnat.delete(self.fulluri, query=query)
        # Make sure there is no cache, this will cause 404 erros on subsequent use
        # of this object, indicating that is has been in fact removed
        self.clearcache()


class XNATListing(Mapping):
    def __init__(self, uri, xnat, secondary_lookup_field, xsiType=None, filter=None):
        # Cache fields
        self._cache = {}
        self.caching = True

        # Important for communication
        self._xnat = xnat
        self._uri = uri
        self._xsiType = xsiType

        # List specific things
        self.secondary_lookup_field = secondary_lookup_field
        self._used_filters = filter or {}

    @property
    @caching
    def data(self):
        xsi_type = ',xsiType' if self._xsiType is None else ''
        columns = 'ID,URI,{}{}'.format(self.secondary_lookup_field, xsi_type)
        query = dict(self.used_filters)
        query['columns'] = columns
        result = self.xnat.get_json(self.uri, query=query)['ResultSet']['Result']
        if not all('URI' in x for x in result):
            # HACK: This is a Resource, that misses the URI and ID field (let's fix that)
            for entry in result:
                if not 'URI' in entry:
                    entry['URI'] = '{}/{}'.format(self.uri, entry['label'])
                if not 'ID' in entry:
                    entry['ID'] = entry['xnat_abstractresource_id']

        elif not all('ID' in x for x in result):
            # HACK: This is a File and it misses an ID field and has Name (let's fix that)
            for entry in result:
                if not 'ID' in entry:
                    entry['ID'] = '{}/files/{}'.format(entry['cat_ID'], entry['Name'])
                    entry['name'] = entry['Name']

        # Post filter result if server side query did not work
        result = [x for x in result if all(fnmatch.fnmatch(x.get(k), v) for k, v in self.used_filters.items())]

        # Create object dictionary
        return {x['ID']: self.xnat.create_object(x['URI'], type_=x.get('xsiType', self._xsiType), id_=x['ID'], **{self.secondary_lookup_field: x.get(self.secondary_lookup_field)}) for x in result}

    def __repr__(self):
        content = ', '.join('({}, {}): {}'.format(k, getattr(v, self.secondary_lookup_field), v) for k, v in self.items())
        return '<XNATListing {}>'.format(content)

    def __getitem__(self, item):
        try:
            return self.data[item]
        except KeyError:
            try:
                return next(x for x in self.values() if getattr(x, self.secondary_lookup_field) == item)
            except StopIteration:
                raise KeyError('Could not find ID/label {} in collection!'.format(item))

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def tabulate(self, columns=None, filter=None):
        """
        Create a table (tuple of namedtuples) from this listing. It is possible
        to choose the columns and add a filter to the tabulation.

        :param tuple columns: names of the variables to use for columns
        :param dict filter: update filters to use (form of {'variable': 'filter*'}),
                             setting this option will try to merge the filters and
                             throw an error if that is not possible.
        :return: tabulated data
        :rtype: tuple
        :raises ValueError: if the new filters conflict with the object filters
        """
        if columns is None:
            columns = ('DEFAULT',)

        if filter is None:
            filter = self.used_filters
        else:
            filter = self.merge_filters(self.used_filters, filter)

        query = dict(filter)
        query['columns'] = ','.join(columns)

        result = self.xnat.get_json(self.uri, query=query)
        if len(result['ResultSet']['Result']) > 0:
            result_columns = result['ResultSet']['Result'][0].keys()

            # Retain requested order
            if columns != ('DEFAULT',):
                result_columns = [x for x in columns if x in result_columns]

            # Replace all non-alphanumeric characters with an underscore
            result_columns = [re.sub('[^0-9a-zA-Z]+', '_', s) for s in result_columns]
            rowtype = namedtuple('TableRow', result_columns)

            # Replace all non-alphanumeric characters in each key of the keyword dictionary
            return tuple(rowtype(**{re.sub('[^0-9a-zA-Z]+', '_', k): v for k, v in x.items()}) for x in result['ResultSet']['Result'])
        else:
            return ()

    @property
    def used_filters(self):
        return self._used_filters

    @staticmethod
    def merge_filters(old_filters, extra_filters):
        # First check for conflicting filters
        for key in extra_filters:
            if key in old_filters and old_filters[key] != extra_filters[key]:
                raise ValueError('Trying to redefine filter {key}={oldval} to {key}={newval}'.format(key=key,
                                                                                                     oldval=old_filters[key],
                                                                                                     newval=extra_filters[key]))

        new_filters = dict(old_filters)
        new_filters.update(extra_filters)

        return new_filters

    def filter(self, filters=None, **kwargs):
        """
        Create a new filtered listing based on this listing. There are two way
        of defining the new filters. Either by passing a dict as the first
        argument, or by adding filters as keyword arguments.

        For example::
          >>> listing.filter({'ID': 'A*'})
          >>> listing.filter(ID='A*')

        are equivalent.

        :param dict filters: a dictionary containing the filters
        :param str kwargs: keyword arguments containing the filters
        :return: new filtered XNATListing
        :rtype: XNATListing
        """
        if filters is None:
            filters = kwargs

        new_filters = self.merge_filters(self.used_filters, filters)
        return XNATListing(self.uri, self.xnat, self.secondary_lookup_field, self._xsiType, new_filters)

    @property
    def uri(self):
        return self._uri

    @property
    def xnat(self):
        return self._xnat


class FileData(XNATObject):
    _XSI_TYPE = 'xnat:fileData'

    def __init__(self, uri, xnat, id_=None, datafields=None, name=None):
        super(FileData, self).__init__(uri, xnat, id_=id_, datafields=datafields)
        self._name = name

    @property
    def name(self):
        return self._name

    def delete(self):
        self.xnat.delete(self.uri)

    def download(self, path):
        self.xnat.download(self.uri, path)


class XNAT(object):
    # Class lookup to populate
    XNAT_CLASS_LOOKUP = {
        "xnat:fileData": FileData,
    }

    def __init__(self, server, interface=None, user=None, password=None, keepalive=840):
        self._interface = interface
        self._projects = None
        self._server = urlparse.urlparse(server) if server else None
        self._cache = {}
        self.caching = True
        self._source_code_file = None
        self._services = Services(xnat=self)
        self._prearchive = Prearchive(xnat=self)

        # Set the keep alive settings and spawn the keepalive thread for sending heartbeats
        if isinstance(keepalive, int) and keepalive > 0:
            self._keepalive = True
            self._keepalive_interval = keepalive
        else:
            self._keepalive = False
            self._keepalive_interval = 14 * 60

        self._keepalive_running = False
        self._keepalive_thread = None
        self._keepalive_event = threading.Event()

        # If needed connect here
        self.connect(server=server, user=user, password=password)

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self, server=None, user=None, password=None):
        # If not connected, connect now
        if self.interface is None:
            if server is None:
                raise ValueError('Cannot connect if no server is given')
            print('[INFO] Connecting to server {}'.format(server))
            if self._interface is not None:
                self.disconnect()

            self._server = urlparse.urlparse(server)

            if user is None and password is None:
                print('[INFO] Retrieving login info for {}'.format(self._server.netloc))
                try:
                    user, _, password = netrc.netrc().authenticators(self._server.netloc)
                except TypeError:
                    raise ValueError('Could not retrieve login info for "{}" from the .netrc file!'.format(server))

            self._interface = requests.Session()
            if (user is not None) or (password is not None):
                self._interface.auth = (user, password)

        # Create a keepalive thread
        self._keepalive_running = True
        self._keepalive_thread = threading.Thread(target=self._keepalive_thread_run)
        self._keepalive_thread.daemon = True  # Make sure thread stops if program stops
        self._keepalive_thread.start()

    def disconnect(self):
        # Stop the keepalive thread
        self._keepalive_running = False
        self._keepalive_event.set()

        if self._keepalive_thread is not None:
            if self._keepalive_thread.is_alive():
                self._keepalive_thread.join(3.0)
            self._keepalive_thread = None

        # Kill the session
        if self._server is not None and self._interface is not None:
            self.delete('/data/JSESSION', headers={'Connection': 'close'})

        # Set the server and interface to None
        self._interface = None
        self._server = None

        # If this object is created using an automatically generated file
        # we have to remove it.
        if self._source_code_file is not None:
            source_pyc = self._source_code_file + 'c'
            if os.path.isfile(self._source_code_file):
                os.remove(self._source_code_file)
                self._source_code_file = None
            if os.path.isfile(source_pyc):
                os.remove(source_pyc)

    @property
    def keepalive(self):
        return self._keepalive

    @keepalive.setter
    def keepalive(self, value):
        if isinstance(value, int):
            if value > 0:
                self._keepalive_interval = value
                value = True
            else:
                value = False

        if not isinstance(value, bool):
            raise TypeError('Type should be an integer or boolean!')

        self._keepalive = value

        if self.keepalive:
            # Send a new heartbeat and restart the timer to make sure the interval is correct
            self._keepalive_event.set()
            self.heartbeat()

    def heartbeat(self):
        self.get('/data/JSESSION')

    def _keepalive_thread_run(self):
        # This thread runs until the program stops, it should be inexpensive if not used due to the long sleep time
        while self._keepalive_running:
            # Wait returns False on timeout and True otherwise
            if not self._keepalive_event.wait(self._keepalive_interval):
                if self.keepalive:
                    self.heartbeat()
            else:
                self._keepalive_event.clear()

    @property
    def interface(self):
        return self._interface

    @property
    def uri(self):
        return '/data/archive'

    @property
    def fulluri(self):
        return self.uri

    @property
    def xnat(self):
        return self

    def _check_response(self, response, accepted_status=None, uri=None):
        if accepted_status is None:
            accepted_status = [200, 201, 202, 203, 204, 205, 206]  # All successful responses of HTML
        if response.status_code not in accepted_status or response.text.startswith(('<!DOCTYPE', '<html>')):
            raise XNATResponseError('Invalid response from XNAT for url {} (status {}):\n{}'.format(uri, response.status_code, response.text))

    def get(self, path, format=None, query=None, accepted_status=None):
        accepted_status = accepted_status or [200]
        uri = self._format_uri(path, format, query=query)
        try:
            response = self.interface.get(uri)
        except requests.exceptions.SSLError:
            raise XNATSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def post(self, path, data=None, format=None, query=None, accepted_status=None):
        accepted_status = accepted_status or [200]
        uri = self._format_uri(path, format, query=query)
        try:
            response = self._interface.post(uri, data=data)
        except requests.exceptions.SSLError:
            raise XNATSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def put(self, path, data=None, files=None, format=None, query=None, accepted_status=None):
        accepted_status = accepted_status or [200, 201]
        uri = self._format_uri(path, format, query=query)
        try:
            response = self._interface.put(uri, data=data, files=files)
        except requests.exceptions.SSLError:
            raise XNATSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow created OK or Create status (OK if already exists)
        return response

    def delete(self, path, headers=None, accepted_status=None, query=None):
        accepted_status = accepted_status or [200]
        uri = self._format_uri(path, query=query)
        try:
            response = self.interface.delete(uri, headers=headers)
        except requests.exceptions.SSLError:
            raise XNATSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def _format_uri(self, path, format=None, query=None):
        if path[0] != '/':
            raise ValueError('The requested URI path should start with a / (e.g. /data/projects), found {}'.format(path))

        if query is None:
            query = {}

        if format is not None:
            query['format'] = format

        # Create the query string
        if len(query) > 0:
            query_string = urllib.urlencode(query)
        else:
            query_string = ''

        data = (self._server.scheme,
                self._server.netloc,
                self._server.path.rstrip('/') + path,
                '',
                query_string,
                '')

        return urlparse.urlunparse(data)

    def get_json(self, uri, query=None):
        response = self.get(uri, format='json', query=query)
        try:
            return response.json()
        except ValueError:
            raise ValueError('Could not decode JSON from {}'.format(response.text))

    def download_stream(self, uri, target_stream, format=None, verbose=True, chunk_size=524288):
        uri = self._format_uri(uri, format=format)

        # Stream the get and write to file
        response = self.interface.get(uri, stream=True)

        if response.status_code != 200:
            raise ValueError('Invalid response from XNAT (status {}):\n{}'.format(response.status_code, response.text))

        bytes_read = 0
        if verbose:
            print('Downloading {}:'.format(uri))
        for chunk in response.iter_content(chunk_size):
            if bytes_read == 0 and chunk.startswith(('<!DOCTYPE', '<html>')):
                raise ValueError('Invalid response from XNAT (status {}):\n{}'.format(response.status_code, chunk))

            bytes_read += len(chunk)
            target_stream.write(chunk)

            if verbose:
                sys.stdout.write('\r{:d} kb'.format(bytes_read / 1024))
                sys.stdout.flush()

    def download(self, uri, target, format=None, verbose=True):
        with open(target, 'wb') as out_fh:
            self.download_stream(uri, out_fh, format=format, verbose=verbose)

        if verbose:
            sys.stdout.write('\nSaved as {}...\n'.format(target))
            sys.stdout.flush()

    def download_zip(self, uri, target, verbose=True):
        self.download(uri, target, format='zip', verbose=verbose)

    def upload(self, uri, file_, retries=1, query=None, content_type=None, method='put'):
        uri = self._format_uri(uri, query=query)
        attempt = 0
        file_handle = None
        opened_file = False

        try:
            while attempt < retries:
                if isinstance(file_, file):
                    # File is open file handle, seek to 0
                    file_handle = file_
                    file_.seek(0)
                    filename = os.path.basename(uri)
                elif os.path.isfile(file_):
                    # File is str path to file
                    file_handle = open(file_, 'rb')
                    opened_file = True
                    filename = os.path.basename(file_)
                else:
                    # File is data to upload
                    file_handle = file_
                    filename = os.path.basename(uri)

                attempt += 1

                try:
                    if content_type is None:
                        files = {filename: file_handle}
                    else:
                        files = {filename: (filename, file_handle, content_type)}
                    if method == 'put':
                        response = self.interface.put(uri, files=files)
                    elif method == 'post':
                        response = self.interface.post(uri, files=files)
                    else:
                        raise ValueError('Invalid upload method "{}" should be either put or post.'.format(method))
                    self._check_response(response)
                    return response
                except XNATResponseError:
                    pass
        finally:
            if opened_file:
                file_handle.close()

        # We didn't return correctly, so we have an error
        raise XNATUploadError('Upload failed after {} attempts! Status code {}, response text {}'.format(retries, response.status_code, response.text))

    @property
    def scanners(self):
        """
        A list of scanners referenced in XNAT
        """
        return [x['scanner'] for x in self.xnat.get_json('/data/archive/scanners')['ResultSet']['Result']]

    @property
    def scan_types(self):
        """
         A list of scan types associated with this XNAT instance
        """
        return self.xnat.get_json('/data/archive/scan_types')['ResultSet']['Result']

    @property
    def xnat_version(self):
        return self.get('/data/version').text

    def create_object(self, uri, type_=None, **kwargs):
        if type_ is None:
            data = self.xnat.get_json(uri)
            type_ = data['items'][0]['meta']
            datafields = data['items'][0]['data_fields']
        else:
            datafields = None

        if type_ not in self.XNAT_CLASS_LOOKUP:
            raise KeyError('Type {} unknow to this XNAT REST client (see XNAT_CLASS_LOOKUP class variable)'.format(type_))

        return self.XNAT_CLASS_LOOKUP[type_](uri, self, datafields=datafields, **kwargs)

    @property
    @caching
    def projects(self):
        return XNATListing(self.uri + '/projects', xnat=self.xnat, secondary_lookup_field='name', xsiType='xnat:projectData')

    @property
    @caching
    def subjects(self):
        return XNATListing(self.uri + '/subjects', xnat=self.xnat, secondary_lookup_field='label', xsiType='xnat:subjectData')

    @property
    @caching
    def experiments(self):
        return XNATListing(self.uri + '/experiments', xnat=self.xnat, secondary_lookup_field='label')

    @property
    def prearchive(self):
        return self._prearchive

    @property
    def services(self):
        return self._services

    def clearcache(self):
        self._cache.clear()


# Services
class Services(object):
    def __init__(self, xnat):
        self._xnat = xnat

    @property
    def xnat(self):
        return self._xnat

    def import_(self, path, overwrite=None, quarantine=False, destination=None, project=None, content_type=None):
        query = {}
        if overwrite is not None:
            if overwrite not in ['none', 'append', 'delete']:
                raise ValueError('Overwrite should be none, append or delete!')
            query['overwrite'] = overwrite

        if quarantine:
            query['quarantine'] = 'true'

        if destination is not None:
            query['dest'] = destination

        if project is not None:
            query['project'] = project

        # Get mimetype of file
        if content_type is None:
            content_type, transfer_encoding = mimetypes.guess_type(path)

        uri = '/data/services/import'
        response = self.xnat.upload(uri=uri, file_=path, query=query, content_type=content_type, method='post')
        return response

        # TODO: figure out why the returned url is not valid!
        #if response.status_code != 200:
        #    raise XNATResponseError('The response for uploading was ({}) {}'.format(response.status_code, response.text))

        #return self.xnat.create_object(response.text)


# Pre-archive
class PrearchiveSession(XNATObject):
    @property
    def id(self):
        return '{}/{}/{}'.format(self.data['project'], self.data['timestamp'], self.data['name'])

    @property
    @caching
    def fulldata(self):
        return self.xnat.get_json(self.uri)['ResultSet']['Result'][0]

    @property
    def data(self):
        return self.fulldata

    @property
    def autoarchive(self):
        return self.data['autoarchive']

    @property
    def folder_name(self):
        return self.data['folderName']

    @property
    def lastmod(self):
        lastmod_string = self.data['lastmod']
        return datetime.datetime.strptime(lastmod_string, '%Y-%m-%d %H:%M:%S.%f')

    @property
    def name(self):
        return self.data['name']

    @property
    def label(self):
        return self.name

    @property
    def prevent_anon(self):
        return self.data['prevent_anon']

    @property
    def prevent_auto_commit(self):
        return self.data['prevent_auto_commit']

    @property
    def project(self):
        return self.data['project']

    @property
    def scan_date(self):
        try:
            return to_date(self.data['scan_date'])
        except isodate.ISO8601Error:
            return None

    @property
    def scan_time(self):
        try:
            return to_time(self.data['scan_time'])
        except isodate.ISO8601Error:
            return None

    @property
    def status(self):
        return self.data['status']

    @property
    def subject(self):
        return self.data['subject']

    @property
    def tag(self):
        return self.data['tag']

    @property
    def timestamp(self):
        return self.data['timestamp']

    @property
    def uploaded(self):
        uploaded_string = self.data['uploaded']
        try:
            return datetime.datetime.strptime(uploaded_string, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return None

    @property
    @caching
    def scans(self):
        data = self.xnat.get_json(self.uri + '/scans')
        # We need to prepend /data to our url (seems to be a bug?)

        return [PrearchiveScan('{}/scans/{}'.format(self.uri, x['ID']),
                               self.xnat,
                               datafields=x) for x in data['ResultSet']['Result']]

    def download(self, path):
        self.xnat.download_zip(self.uri, path)
        return path

    def archive(self, overwrite=None, quarantine=None, trigger_pipelines=None, destination=None):
        query = {'src': self.uri}

        if overwrite is not None:
            if overwrite not in ['none', 'append', 'delete']:
                raise ValueError('Overwrite should be none, append or delete!')
            query['overwrite'] = overwrite

        if quarantine is not None:
            if isinstance(quarantine, bool):
                if quarantine:
                    query['quarantine'] = 'true'
                else:
                    query['quarantine'] = 'false'
            else:
                raise TypeError('Quarantine should be a boolean')

        if trigger_pipelines is not None:
            if isinstance(trigger_pipelines, bool):
                if trigger_pipelines:
                    query['triggerPipelines'] = 'true'
                else:
                    query['triggerPipelines'] = 'false'
            else:
                raise TypeError('trigger_pipelines should be a boolean')

        if destination is not None:
            query['dest'] = destination

        return self.xnat.post('/data/services/archive', query=query)

    def delete(self, async=None):
        query = {'src': self.uri}

        if async is not None:
            if isinstance(async, bool):
                if async:
                    query['async'] = 'true'
                else:
                    query['async'] = 'false'
            else:
                raise TypeError('async should be a boolean')

        return self.xnat.post('/data/services/prearchive/delete', query=query)

    def rebuild(self, async=None):
        query = {'src': self.uri}

        if async is not None:
            if isinstance(async, bool):
                if async:
                    query['async'] = 'true'
                else:
                    query['async'] = 'false'
            else:
                raise TypeError('async should be a boolean')

        return self.xnat.post('/data/services/prearchive/rebuild', query=query)

    def move(self, new_project, async=None):
        query = {'src': self.uri,
                 'newProject': new_project}

        if async is not None:
            if isinstance(async, bool):
                if async:
                    query['async'] = 'true'
                else:
                    query['async'] = 'false'
            else:
                raise TypeError('async should be a boolean')

        return self.xnat.post('/data/services/prearchive/move', query=query)


class PrearchiveScan(XNATObject):
    def __init__(self, uri, xnat, id_=None, datafields=None, parent=None, fieldname=None):
        super(PrearchiveScan, self).__init__(uri=uri,
                                             xnat=xnat,
                                             id_=id_,
                                             datafields=datafields,
                                             parent=parent,
                                             fieldname=fieldname)

        self._fulldata = {'data_fields': datafields}

    @property
    def series_description(self):
        return self.data['series_description']

    def download(self, path):
        self.xnat.download_zip(self.uri, path)
        return path

    @property
    def fulldata(self):
        return self._fulldata


class Prearchive(object):
    def __init__(self, xnat):
       self._xnat = xnat

    @property
    def xnat(self):
        return self._xnat

    def sessions(self, project=None):
        if project is None:
            uri = '/data/prearchive/projects'
        else:
            uri = '/data/prearchive/projects/{}'.format(project)

        data = self.xnat.get_json(uri)
        # We need to prepend /data to our url (seems to be a bug?)
        return [PrearchiveSession('/data{}'.format(x['url']), self.xnat) for x in data['ResultSet']['Result']]
