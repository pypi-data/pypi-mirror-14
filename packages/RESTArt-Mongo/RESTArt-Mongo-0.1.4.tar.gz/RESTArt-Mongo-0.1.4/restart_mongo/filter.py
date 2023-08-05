from __future__ import absolute_import

import functools


def query_params(*names):
    """A helper decorator for binding query parameters specified by
    `names` as arguments to `query_<name>` methods.

    For example:

        class UserFilter(Filter):
            @query_params('username')
            def query_username(self, username):
                return {'username': username.upper()}

            @query_params('date_joined_gt', 'date_joined_lt')
            def query_datejoined(self, date_joined_gt=None, date_joined_lt=None):
                conditions = {}
                if date_joined_gt:
                    conditions.update({'$gt': date_joined_gt})
                if date_joined_lt:
                    conditions.update({'$lt': date_joined_lt})
                if conditions:
                    return {'date_joined': conditions}
                else:
                    return {}
    """
    def wrapper(method):
        @functools.wraps(method)
        def decorator(self, params):
            kwargs = {}
            for name in names:
                if name in params:
                    value = params.pop(name)
                    kwargs.update({name: value})
            try:
                return method(self, **kwargs)
            except TypeError:
                return {}
        return decorator

    return wrapper


class Filter(object):
    """The Class used for customized filtering.

    1. Raw query parameter

    Raw query parameter supports simple filtering:

        /users?name=russellluo

    Note that the MongoDB-style nested field names are also supported):

        /users?name=russellluo&address.country=China

    2. The `Filter` class (and its subclasses)

    The `Filter` class (and its subclasses) supports user-defined methods for customized filtering:

        1. override `query` method
        2. add `query_<name>` method

        All methods should return MongoDB-style conditions.

    For example,
    """

    def __init__(self, database, collection_name):
        self.database = database
        self.collection_name = collection_name

    def merge(self, conditions):
        """Merge `conditions` using AND-logic into one condition."""
        if conditions:
            return {'$and': conditions}
        else:
            return {}

    def query(self, params):
        """Generate lookup conditions."""
        conditions = []

        # Collect conditions from `query_<name>` methods
        for attr_name in dir(self):
            if attr_name.startswith('query_'):
                method = getattr(self, attr_name)
                condition = method(params)
                if condition:
                    conditions.append(condition)

        # Also treat remaining `params` as conditions
        if params:
            conditions.append(params)

        return self.merge(conditions)
