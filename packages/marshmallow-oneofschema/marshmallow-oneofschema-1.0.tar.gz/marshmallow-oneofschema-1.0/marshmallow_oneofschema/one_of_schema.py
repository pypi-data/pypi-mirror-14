from marshmallow import Schema, MarshalResult, UnmarshalResult


class OneOfSchema(Schema):
    """
    This is a special kind of schema that actually multiplexes other schemas
    based on object type. When serializing values, it uses get_obj_type() method
    to get object type name. Then it uses `type_schemas` name-to-Schema mapping
    to get schema for that particular object type, serializes object using that
    schema and adds an extra "type" field with name of object type.
    Deserialization is reverse.

    Example:

        class Foo(object):
            def __init__(self, foo):
                self.foo = foo

        class Bar(object):
            def __init__(self, bar):
                self.bar = bar

        class FooSchema(marshmallow.Schema):
            foo = marshmallow.fields.String(required=True)

            @marshmallow.post_load
            def make_foo(self, data):
                return Foo(**data)

        class BarSchema(marshmallow.Schema):
            bar = marshmallow.fields.Integer(required=True)

            @marshmallow.post_load
            def make_bar(self, data):
                return Bar(**data)

        class MyUberSchema(marshmallow.OneOfSchema):
            type_schemas = {
                'foo': FooSchema,
                'bar': BarSchema,
            }

            def get_obj_type(self, obj):
                if isinstance(obj, Foo):
                    return 'foo'
                elif isinstance(obj, Bar):
                    return 'bar'
                else:
                    raise Exception('Unknown object type: %s' % repr(obj))

        MyUberSchema().dump([Foo(foo='hello'), Bar(bar=123)], many=True).data
        # => [{'type': 'foo', 'foo': 'hello'}, {'type': 'bar', 'bar': 123}]

    You can control type field name added to serialized object representation by
    setting `type_field` class property.
    """
    type_field = 'type'
    type_schemas = []

    def get_obj_type(self, obj):
        """Returns name of object schema"""
        return obj.__class__.__name__

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        if not many:
            return self._dump(obj, update_fields, **kwargs)

        result_data = []
        result_errors = {}

        for idx, o in enumerate(obj):
            result = self._dump(o, update_fields, **kwargs)
            result_data.append(result.data)
            if result.errors:
                result_errors[idx] = result.errors

        return MarshalResult(result_data, result_errors)

    def _dump(self, obj, update_fields=True, **kwargs):
        obj_type = self.get_obj_type(obj)
        if not obj_type:
            return MarshalResult(None, {
                '_schema': 'Unknown object class: %s' % obj.__class__.__name__
            })

        type_schema = self.type_schemas.get(obj_type)
        if not type_schema:
            return MarshalResult(None, {
                '_schema': 'Unsupported object type: %s' % obj_type
            })

        schema = (type_schema if isinstance(type_schema, Schema)
                  else type_schema())
        result = schema.dump(
            obj, many=False, update_fields=update_fields, **kwargs
        )
        if result.data:
            result.data[self.type_field] = obj_type
        return result

    def load(self, data, many=None, partial=None):
        if not many:
            return self._load(data, partial=partial)

        result_data = []
        result_errors = {}

        for idx, item in enumerate(data):
            result = self._load(item, partial=partial)
            result_data.append(result.data)
            if result.errors:
                result_errors[idx] = result.errors

        return UnmarshalResult(result_data, result_errors)

    def _load(self, data, partial=None):
        data_type = data.get(self.type_field)
        if not data_type:
            return UnmarshalResult({}, {
                self.type_field: [u'Missing data for required field.']
            })

        type_schema = self.type_schemas.get(data_type)
        if not type_schema:
            return UnmarshalResult({}, {
                self.type_field: ['Unsupported value: %s' % data_type],
            })

        schema = (type_schema if isinstance(type_schema, Schema)
                  else type_schema())
        return schema.load(data, many=False, partial=partial)

    def validate(self, data, many=None, partial=None):
        return self.load(data, many=many, partial=partial).errors
