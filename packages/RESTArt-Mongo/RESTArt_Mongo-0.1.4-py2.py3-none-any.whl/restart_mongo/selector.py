from __future__ import absolute_import


class Selector(object):
    """The class for selecting which fields are returned.

    This class supports the keyword `fields` in query parameter.

    For example, the following request will receive all users with only
    `name` and `password` fields in each user:

        /users?fields=name,password

    Note that the MongoDB-style nested field names are also supported:

        /users?fields=name,address.country
    """

    def get_raw(self, query_params):
        """Get the raw fields specified in the query parameters."""
        fields = query_params.pop('fields', None)
        if fields is None:
            raw = None
        else:
            raw = fields.split(',')
        return raw

    def get_fields(self, query_params):
        """Get the MongoDB-style fields from the query parameters."""
        raw = self.get_raw(query_params)
        if raw is None:
            return None

        fields = {
            field_name: True
            for field_name in raw
        }
        if raw and '_id' not in raw:
            fields.update({'_id': False})
        return fields
