import json

import yaml

class Converter(object):
  """
  A converter turns a jsonschema `schema` into 
  another format.
  """

  def __init__(self):
    pass

  def to(self, schema, **kw):
    """
    Default json-schema serializer.
    """
    return schema.body


class JsonConverter(Converter):
  """
  Simple Json Converter
  """
  def to(self, schema, **kw):
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', True)
    return json.dumps(schema.body, **kw)


class YamlConverter(Converter):

  def to(self, schema, **kw):
    """
    Dump JSON schema to Yaml.
    """
    return yaml.safe_dump(schema.body, default_flow_style=False)


class AvroConverter(Converter):
  """
  Convert json schema dict to avsc format
  https://avro.apache.org/docs/1.7.7/spec.html#schemas
  
  """
  TYPE_MAP = {
    'boolean': 'boolean',
    'number': 'double',
    'integer': 'long',
    'string': 'string',
    'date-time': 'string',
    'null': 'null'
  }

  def to(self, schema, **kw):
    """
    Map json-schema to avsc
    """
    return self.to_avro(schema, **kw)

  def to_avro(self, schema, **kw):
    """
    core function
    """
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', False)
    fields = self._map_properties_to_fields(
      schema.body['properties'], **kw)
    
    return {
      'name': "{0}_rec".format(schema.body['title']),
      'type': 'record',
      'doc': '{0} avro schema'.format(schema.body['title']),
      'fields': fields
    }

  def _map_properties_to_fields(self, props, **kw):
    """
    Recursively map properties to a list of avsc fields.
    """
    fields = []
    for name, prop in props.items():
      types = prop.get('type', [])
      if not isinstance(types, list):
        types = [types]

      # recurse on objects
      if types[0] == 'object':
        rec = self._init_obj_record(name)
        rec['type']['fields'] = self._map_properties_to_fields(prop['properties'])
      
      # arrays
      elif types[0] == 'array':
        types = prop.get('items', {}).get('type', [])
        
        # array of objects
        if 'object' in types:
          rec = self._init_array_of_records(name)
          fs = self._map_properties_to_fields(
            prop['items']['properties'])
          rec['type']['items']['fields'] = fs

        # array of simple types:
        else:
          rec = self._init_simple_array(
            name, self._map_types(types))

      elif any([t in self.TYPE_MAP for t in types]):
        rec = self._init_field(name, self._map_types(types))

      fields.append(rec)
    return fields

  def _map_types(self, types):
    """
    Map simple types 
    """
    return [self.TYPE_MAP.get(t) for t in types]

  def _init_field(self, name, types):
    """
    initialize an avsc field.
    """
    return {
      "name": name,
      "default": None,
      "type": types
    }

  def _init_record(self, name):
    """
    initialize an avsc record
    """
    return { 
        "type": "record", 
        "name": "{0}_rec".format(name),
        "fields":[]
      }

  def _init_obj_record(self, name):
    """
    initialize an avsc record
    """
    return { 
        "name": name,
        "default": {},
        "type": self._init_record(name)
      }

  def _init_simple_array(self, name, types):
    """
    initialize an avsc simple array
    """
    return {
      "name": name,
      "default": [],
      "type": {
        "type": "array",
        "items": types
      }
    } 

  def _init_array_of_records(self, name):
    """
    initialize an avsc array of records
    """
    return {
      "name": name,
      "default": [],
      "type": {
        "type": "array",
        "items": self._init_record(name)
      }
    }

class AvscConverter(AvroConverter):
  """
  simple json wrapper of avro converter
  """

  def to(self, schema, **kw):
    """
    Dump Avro Schema as Avsc
    """
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', True)
    return json.dumps(self.to_avro(schema, **kw), **kw)

class ElasticSearchConverter(Converter):
  
  """
  https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
  """ 
  
  TYPE_MAP = {
    'boolean': 'boolean',
    'number': 'double',
    'string': 'string',
    'integer': 'integer',
    'date-time': 'date'
  }

  def to(self, schema, **kw):
    """
    Format jsonschema as elasticsearch dictionary.
    """
    return self.to_elasticsearch(schema, **kw)

  def to_elasticsearch(self, schema, **kw):
    """
    Map json schema to elasticsearch mapping schema.
    """
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', False)
    properties = self._map_properties(schema.body['properties'])
    return {
      schema.body.get('title'): {
        'properties': properties
      }
    }

  def _map_properties(self, properties):
    """
    map json scheam properties to elasticsearch properties
    """
    props = {}
    for name, prop in properties.items():
      types = prop.get('type')
      if not isinstance(types, list):
        types = [types]

      type = [t for t in types if t!='null'][0]

      # recurse on objects
      if type == 'object':

        rec = self._init_object(name)
        rec[name].update(self._map_properties(prop['properties']))
      
      # nested arrays
      elif type == 'array' and 'object' in prop['items'].get('type'):
        rec = self._init_array_of_records(name)

      else:
        rec = self._init_field(name, type)

      # set property
      props.update(rec)
    return props

  def _init_field(self, name, type):
    """
    initialize an avsc field.
    """
    type = self.TYPE_MAP.get(type, 'string')
    return {name: {"type": type}}

  def _init_object(self, name):
    """
    initialize an es object type.
    """
    return {name: {}}

  def _init_array_of_records(self, name):
    """
    initialize an avsc array of records
    """
    return {name: {"type": "nested"}}


class ElasticSearchJsonConverter(ElasticSearchConverter):

  def to(self, schema, **kw):
    """
    ElasticSearch json converter, 
    """
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', True)
    schema = self.to_elasticsearch(schema, **kw)
    return json.dumps(schema, **kw)


class ElasticSearchYamlConverter(ElasticSearchConverter):

  def to(self, schema, **kw):
    """
    ElasticSearch yaml converter, 
    """
    kw.setdefault('indent', 2)
    kw.setdefault('sort_keys', True)
    schema = self.to_elasticsearch(schema, **kw)
    return yaml.safe_dump(schema, default_flow_style=False)