""" These are utility functions used by the OCCRP datamapper to generate a
matching ElasticSearch schema, given a JSON Schema descriptor. """
from jsonmapping.visitor import SchemaVisitor


def generate_schema_mapping(resolver, schema_uri, depth=1):
    """ Try and recursively iterate a JSON schema and to generate an ES mapping
    that encasulates it. """
    visitor = SchemaVisitor({'$ref': schema_uri}, resolver)
    return _generate_schema_mapping(visitor, set(), depth)


def _generator_field_mapping(visitor):
    type_name = 'string'
    if 'number' in visitor.types:
        type_name = 'float'
    if 'integer' in visitor.types:
        type_name = 'long'
    if 'boolean' in visitor.types:
        type_name = 'boolean'
    mapping = {'type': type_name, 'index': 'not_analyzed'}
    format_ = visitor.schema.get('format')
    if format_ and format_ in ('date-time', 'datetime', 'date'):
        mapping['type'] = 'date'
        mapping['format'] = 'dateOptionalTime'
    return mapping


def _generate_schema_mapping(visitor, path, depth):
    if visitor.is_object:
        mapping = {
            'type': 'nested',
            '_id': {'path': 'id'},
            'properties': {
                '$schema': {'type': 'string', 'index': 'not_analyzed'},
                'id': {'type': 'string', 'index': 'not_analyzed'}
            }
        }
        if not visitor.parent:
            mapping['type'] = 'object'
        if visitor.path in path or not depth:
            return mapping
        sub_path = path.union([visitor.path])
        for prop in visitor.properties:
            prop_mapping = _generate_schema_mapping(prop, sub_path, depth - 1)
            mapping['properties'][prop.name] = prop_mapping
        return mapping
    elif visitor.is_array:
        return _generate_schema_mapping(visitor.items, path, depth - 1)
    else:
        return _generator_field_mapping(visitor)
