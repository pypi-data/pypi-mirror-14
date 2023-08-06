import uuid
from collections import Mapping
import typecast

from jsonmapping.visitor import SchemaVisitor


TYPE_SCHEMA = '$schema'
TYPE_LINK = 'link'


class StatementsVisitor(SchemaVisitor):
    """ This class has utility functions for transforming JSON schema defined
    objects into a series of RDF-like statements (i.e. subject, predicate,
    object, context) quads. It can be used independently of any specific
    storage backend, including RDF. """

    @property
    def subject(self):
        return self.schema.get('rdfSubject', 'id')

    def get_subject(self, data):
        """ Try to get a unique ID from the object. By default, this will be
        the 'id' field of any given object, or a field specified by the
        'rdfSubject' property. If no other option is available, a UUID will be
        generated. """
        if not isinstance(data, Mapping):
            return None
        if data.get(self.subject):
            return data.get(self.subject)
        return uuid.uuid4().urn

    @property
    def predicate(self):
        return self.schema.get('rdfName', self.name)

    @property
    def reverse(self):
        """ Reverse links make sense for object to object links where we later
        may want to also query the reverse of the relationship, e.g. when obj1
        is a child of obj2, we want to infer that obj2 is a parent of obj1. """
        name = self.schema.get('rdfReverse')
        if name is not None:
            return name
        if self.parent is not None and self.parent.is_array:
            return self.parent.reverse

    def get_property(self, predicate):
        for prop in self.properties:
            if predicate == prop.name:
                return prop

    def triplify(self, data, parent=None):
        """ Recursively generate statements from the data supplied. """
        if data is None:
            return

        if self.is_object:
            for res in self._triplify_object(data, parent):
                yield res
        elif self.is_array:
            for item in data:
                for res in self.items.triplify(item, parent):
                    yield res
        else:
            # TODO: figure out if I ever want to check for reverse here.
            type_name = typecast.name(data)
            obj = typecast.stringify(type_name, data)
            if obj is not None:
                obj = obj.strip()
            yield (parent, self.predicate, obj, type_name)

    def _triplify_object(self, data, parent):
        """ Create bi-directional statements for object relationships. """
        subject = self.get_subject(data)
        if self.path:
            yield (subject, TYPE_SCHEMA, self.path, TYPE_SCHEMA)

        if parent is not None:
            yield (parent, self.predicate, subject, TYPE_LINK)
            if self.reverse is not None:
                yield (subject, self.reverse, parent, TYPE_LINK)

        for prop in self.properties:
            for res in prop.triplify(data.get(prop.name), subject):
                yield res

    # Clever Method Names Award, 2014 and two years running
    def objectify(self, load, node, depth=2, path=None):
        """ Given a node ID, return an object the information available about
        this node. This accepts a loader function as it's first argument, which
        is expected to return all tuples of (predicate, object, source) for
        the given subject. """
        if path is None:
            path = set()

        if self.is_object:
            if depth < 1:
                return
            return self._objectify_object(load, node, depth, path)
        elif self.is_array:
            if depth < 1:
                return
            return [self.items.objectify(load, node, depth, path)]
        else:
            return node

    def _objectify_object(self, load, node, depth, path):
        # Support inline objects which don't count towards the depth.
        next_depth = depth
        if not self.schema.get('inline'):
            next_depth = depth - 1

        sub_path = path.union([node])
        obj = {
            self.subject: node,
            '$schema': self.path,
            '$sources': [],
            '$collections': [],
            '$authors': [],
            '$attrcount': 0,
            '$linkcount': 0,
        }
        for stmt in load(node):
            prop = self.get_property(stmt['predicate'])
            if prop is None:
                continue
            if stmt['object'] in path and not prop.is_value:
                continue
            if prop.name not in obj:
                obj['$attrcount'] += 1
                if stmt['type'] == TYPE_LINK:
                    obj['$linkcount'] += 1

            if stmt.get('source') and \
                    stmt.get('source') not in obj['$sources']:
                obj['$sources'].append(stmt.get('source'))

            if stmt.get('collection') and \
                    stmt.get('collection') not in obj['$collections']:
                obj['$collections'].append(stmt.get('collection'))

            if stmt.get('author') and \
                    stmt.get('author') not in obj['$authors']:
                obj['$authors'].append(stmt.get('author'))

            value = prop.objectify(load, stmt['object'], next_depth, sub_path)
            if value is None:
                continue

            if prop.is_array and prop.name in obj:
                obj[prop.name].extend(value)
            else:
                obj[prop.name] = value
        return obj
