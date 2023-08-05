"""
Collection of exceptions that may be encountered when using the query_dict class
and performing queries on dicts.
"""


class InvalidQueryException(Exception):
    """
    Exception thrown if a query is found to be syntactically invalid.
    This is caused by incorrect characters and empty components of a
    search string.
    """
    pass


class EmptyQueryException(InvalidQueryException):
    """
    Exception thrown if a query is found to be an empty string.
    """
    pass

class InvalidFilterException(Exception):
    """
    Exception thrown if the specified filter callback is not a callable
    method. If this is encountered, ensure you are not invoking your callback,
    e.g.: filter=callback(), it should be: filter=callback
    """