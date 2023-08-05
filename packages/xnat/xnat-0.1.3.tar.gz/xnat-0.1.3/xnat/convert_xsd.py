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

import contextlib
import inspect
import keyword
import re

import xnatbases


class ClassRepresentation(object):
    # Override strings for certain properties
    SUBSTITUTIONS = {
            "fields": "    @property\n    def fields(self):\n        return self._fields",
            }

    # Fields for lookup besides the id
    SECONDARY_LOOKUP_FIELDS = {
            "projectData": "name",
            "subjectData": "label",
            "experimentData": "label",
            "imageScanData": "type",
            "abstractResource": "label"
            }

    def __init__(self, parser, name):
        self.parser = parser
        self.name = name
        self.baseclass = 'XNATObject'
        self.properties = {}

    def __repr__(self):
        return '<Class {}({})>'.format(self.name, self.baseclass)

    def __str__(self):
        base = self.get_base_template()
        if base is not None:
            base_source = inspect.getsource(base)
            base_source = re.sub(r'class {}\(XNATObject\):'.format(self.python_name), 'class {}({}):'.format(self.python_name, self.python_baseclass), base_source)
            header = base_source.strip() + '\n\n'
        else:
            header = '# No base template found for {}\n'.format(self.python_name)
            header += "class {name}({base}):\n".format(name=self.python_name, base=self.python_baseclass)

        if 'fields' in self.properties:
            header += "    _HAS_FIELDS = True\n"
        header += "    _XSI_TYPE = 'xnat:{}'\n\n".format(self.name)

        if self.name in self.SECONDARY_LOOKUP_FIELDS:
            header += self.init

        properties = [self.properties[k] for k in sorted(self.properties.keys())]

        properties = '\n\n'.join(self.print_property(p) for p in properties if not self.hasattr(p.clean_name))
        return '{}{}'.format(header, properties)

    def hasattr(self, name):
        base = self.get_base_template()

        if base is not None:
            return hasattr(base, name)
        else:
            base = self.parser.class_list.get(self.baseclass)
            if base is not None:
                return base.hasattr(name)
            else:
                return False

    @property
    def python_name(self):
        return self.name[0].upper() + self.name[1:]

    @property
    def python_baseclass(self):
        return self.baseclass[0].upper() + self.baseclass[1:]

    def get_base_template(self):
        if hasattr(xnatbases, self.python_name):
            return getattr(xnatbases, self.python_name)

    def print_property(self, prop):
        if prop.name in self.SUBSTITUTIONS:
            return self.SUBSTITUTIONS[prop.name]
        else:
            data = str(prop)
            if prop.name == self.SECONDARY_LOOKUP_FIELDS.get(self.name, '!None'):
                head, tail = data.split('\n', 1)
                data = '{}\n    @caching\n{}'.format(head, tail)
            return data

    @property
    def init(self):
        if self.name in self.SECONDARY_LOOKUP_FIELDS:
            return "    def __init__(self, uri, xnat, id_=None, datafields=None, {lookup}=None):\n        super({name}, self).__init__(uri, xnat, id_=id_, datafields=datafields)\n        if {lookup} is not None:\n            self._cache['{lookup}'] = {lookup}\n\n".format(name=self.python_name, lookup=self.SECONDARY_LOOKUP_FIELDS[self.name])
        else:
            return ""


class PropertyRepresentation(object):
    def __init__(self, parser, name, type_=None):
        self.parser = parser
        self.name = name
        self.restrictions = {}
        self.type_ = type_
        self.docstring = None

    def __repr__(self):
        return '<Property {}({})>'.format(self.name, self.type_)

    def __str__(self):
        docstring = '\n        """{}"""'.format(self.docstring) if self.docstring is not None else ''
        if self.type_ is None or not self.type_.startswith('xnat:'):
            return \
        """    @property
    def {clean_name}(self):{docstring}
        # Generate automatically, type: {type}
        return self.get("{name}", type_="{type}")
    
    @ {clean_name}.setter
    def {clean_name}(self, value):{docstring}{restrictions}
        # Generate automatically, type: {type}
        self.set("{name}", value, type_="{type}")""".format(clean_name=self.clean_name, docstring=docstring, name=self.name, type=self.type_, restrictions=self.restrictions_code())
        else:
            return \
        """    @property
    @caching
    def {clean_name}(self):{docstring}
        # Generated automatically, type: {type_}
        return self.get_object("{name}")""".format(clean_name=self.clean_name,
                                                   docstring=docstring,
                                                   name = self.name,
                                                   type_=self.type_)

    @property
    def clean_name(self):
        name = re.sub('[^0-9a-zA-Z]+', '_', self.name)
        if keyword.iskeyword(name):
            name = name + '_'
        return name.lower()

    def restrictions_code(self):
        if len(self.restrictions) > 0:
            data = '\n        # Restrictions for value'
            if 'min' in self.restrictions:
                data += "\n        if value < {min}:\n            raise ValueError('{name} has to be greater than or equal to {min}')\n".format(name=self.name, min=self.restrictions['min'])
            if 'max' in self.restrictions:
                data += "\n        if value > {max}:\n            raise ValueError('{name} has to be smaller than or equal to {max}')\n".format(name=self.name, max=self.restrictions['max'])
            if 'maxlength' in self.restrictions:
                data += "\n        if len(value) > {maxlength}:\n            raise ValueError('length {name} has to be smaller than or equal to {maxlength}')\n".format(name=self.name, maxlength=self.restrictions['maxlength'])
            if 'enum' in self.restrictions:
                data += "\n        if value not in [{enum}]:\n            raise ValueError('{name} has to be one of: {enum}')\n".format(name=self.name, enum=', '.join('"{}"'.format(x) for x in self.restrictions['enum']))

            return data
        else:
            return ''


class SchemaParser(object):
    def __init__(self):
        self.class_list = {}
        self.unknown_tags = set()
        self.new_class_stack = [None]
        self.new_property_stack = [None]

    def __iter__(self):
        visited = set(['XNATObject'])
        tries = 0
        while len(visited) < len(self.class_list) and tries < 50:
            for key, value in self.class_list.items():
                if key in visited:
                    continue

                base = value.baseclass
                if not base.startswith('xs:') and base not in visited:
                    continue

                visited.add(key)
                yield value

            tries += 1

        if len(visited) < len(self.class_list):
            print('Visited: {}, expected: {}'.format(len(visited), len(self.class_list)))
            print('Missed: {}'.format(set(self.class_list.keys()) - visited))

    @contextlib.contextmanager
    def descend(self, new_class=None, new_property=None):
        if new_class is not None:
            self.new_class_stack.append(new_class)
        if new_property is not None:
            self.new_property_stack.append(new_property)

        yield

        if new_class is not None:
            self.new_class_stack.pop()
        if new_property is not None:
            self.new_property_stack.pop()

    @property
    def current_class(self):
        return self.new_class_stack[-1]

    @property
    def current_property(self):
        return self.new_property_stack[-1]

    def parse(self, element):
        if element.tag in self.PARSERS:
            self.PARSERS[element.tag](self, element)
        else:
            self.parse_unknown(element)

    def parse_complex_type(self, element):
        name = element.get('name')

        new_class = ClassRepresentation(self, name)
        self.class_list[name] = new_class
        
        # Descend
        with self.descend(new_class=new_class):
            self.parse_children(element)

    def parse_children(self, element):
        for child in element.getchildren():
            self.parse(child)

    def parse_ignore(self, element):
        pass

    def parse_schema(self, element):
        self.parse_children(element)

    def parse_complex_content(self, element):
        self.parse_children(element)

    def parse_extension(self, element):
        old_base = self.current_class.baseclass 
        new_base = element.get('base')
        if new_base.startswith('xnat:'):
            new_base = new_base[5:]
        if old_base == 'XNATObject':
            self.current_class.baseclass = new_base
        else:
            raise ValueError('Trying to reset base class again from {} to {}'.format(old_base, new_base))

        self.parse_children(element)

    def parse_sequence(self, element):
        self.parse_children(element)

    def parse_simple_type(self, element):
        self.parse_children(element)

    def parse_simple_content(self, element):
        self.parse_children(element)

    def parse_attribute(self, element):
        name = element.get('name')
        type_ = element.get('type')

        if self.current_class is not None:
            new_property = PropertyRepresentation(self, name, type_)
            self.current_class.properties[name] = new_property

            with self.descend(new_property=new_property):
                self.parse_children(element)

    def parse_restriction(self, element):
        old_type = self.current_property.type_
        new_type = element.get('base')

        if old_type is not None:
            raise ValueError('Trying to override a type from a restriction!? (from {} to {})'.format(old_type, new_type))

        self.current_property.type_ = new_type

        self.parse_children(element)

    def parse_maxlength(self, element):
        self.current_property.restrictions['maxlength'] = element.get('value')

    def parse_min_inclusive(self, element):
        self.current_property.restrictions['min'] = element.get('value')

    def parse_max_inclusive(self, element):
        self.current_property.restrictions['max'] = element.get('value')

    def parse_annotation(self, element):
        self.parse_children(element)

    def parse_documentation(self, element):
        if self.current_property is not None:
            self.current_property.docstring = element.text

    def parse_choice(self, element):
        self.parse_children(element)

    def parse_enumeration(self, element):
        if 'enum' in self.current_property.restrictions:
            self.current_property.restrictions['enum'].append(element.get('value'))
        else:
            self.current_property.restrictions['enum'] = [element.get('value')]

    def parse_element(self, element):
        name = element.get('name')
        type_ = element.get('type')

        if self.current_class is not None:
            new_property = PropertyRepresentation(self, name, type_)
            self.current_class.properties[name] = new_property

            with self.descend(new_property=new_property):
                self.parse_children(element)

    def parse_unknown(self, element):
        self.unknown_tags.add(element.tag)

    PARSERS = {
            '{http://www.w3.org/2001/XMLSchema}complexType': parse_complex_type,
            '{http://www.w3.org/2001/XMLSchema}complexContent': parse_complex_content,
            '{http://www.w3.org/2001/XMLSchema}extension': parse_extension,
            '{http://www.w3.org/2001/XMLSchema}sequence': parse_sequence,
            '{http://www.w3.org/2001/XMLSchema}simpleType': parse_simple_type,
            '{http://www.w3.org/2001/XMLSchema}simpleContent': parse_simple_content,
            '{http://www.w3.org/2001/XMLSchema}attribute': parse_attribute,
            '{http://www.w3.org/2001/XMLSchema}restriction': parse_restriction,
            '{http://www.w3.org/2001/XMLSchema}minInclusive': parse_min_inclusive,
            '{http://www.w3.org/2001/XMLSchema}maxInclusive': parse_max_inclusive,
            '{http://www.w3.org/2001/XMLSchema}maxLength': parse_maxlength,
            '{http://www.w3.org/2001/XMLSchema}choice': parse_choice,
            '{http://www.w3.org/2001/XMLSchema}enumeration': parse_enumeration,
            '{http://www.w3.org/2001/XMLSchema}element': parse_element,
            '{http://www.w3.org/2001/XMLSchema}annotation': parse_annotation,
            '{http://www.w3.org/2001/XMLSchema}documentation': parse_documentation,
            '{http://www.w3.org/2001/XMLSchema}schema': parse_schema,
            '{http://www.w3.org/2001/XMLSchema}import': parse_ignore,
            }

