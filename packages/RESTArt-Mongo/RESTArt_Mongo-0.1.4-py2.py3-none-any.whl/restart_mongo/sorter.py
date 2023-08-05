from __future__ import absolute_import


class Sorter(object):
    """The class for sorting.

    This class supports the keyword `sort` in query parameter:

    Sign       | Order
    ---------- | ----------
    + or empty | Ascending
    -          | Descending

    For example, you can sort users first by `name` in ascending-order
    and second by `age` in descending-order::

        /users?sort=name,-age

    Note that the MongoDB-style nested field names are also supported:

        /users?sort=name,address.country
    """

    def get_args(self, query_params):
        sort = query_params.pop('sort', None)
        if sort is None:
            args = None
        else:
            args = [
                (arg[1:], -1) if arg.startswith('-') else (arg, 1)
                for arg in sort.split(',')
            ]
        return args
