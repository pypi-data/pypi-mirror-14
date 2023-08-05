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
