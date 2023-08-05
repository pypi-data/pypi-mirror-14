import itertools
import random
import query_collections.search
from functools import reduce


class query_dict(dict):
    """
    A dictitonary implementation that has the following attributes:
        - query is directly implemented within object
        - dictionary values can be accessed with the dot operator
        via query_dict_instance.key -> returns the value associated with 'key'
    """

    """
    We need delattr and setattr in order to set and delete members
    in a fashion such as dict_instance.name = "cory"
    """

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def get(self, k, d=None):
        item = super().get(k, d)
        if item:
            if isinstance(item, list):
                return query_list(item)
            elif isinstance(item, dict):
                return query_dict(item)
            else:
                return item
        else:
            return None

    def __getattr__(self, item):
        return self.get(item)

    def __getattribute__(self, item):
        recv_item = super().__getattribute__(item)
        if not callable(recv_item) and item in self:
            return self.get(item)
        return recv_item

    def __getitem__(self, item):
        """
        Allows us to execute queries on a dict or list by simply
        adding a '?' before the query when using braces to access
        a member. If a question mark is not present, assume
        that we are attempting to access a member of the dict.

        e.g.: queried_item = dict_instance['?list:0']
        """
        if isinstance(item, str):
            if item.find('?', 0, 1) == 0:
                return self.query(item[1:])

        # otherwise act as normal
        return self.get(item)

    def query(self, query_string, filters=None):
        """
        Performs a query search with 'query_string' as the search
        string
        :param query_string: Search string to access desired member(s)
        :param filters: Filter methods to perform on the result preceding
        the filter operator
        :return: object(s) if exists, otherwise exception is thrown
        """
        return query_collections.search.query(self, query_string, filters=filters)

    def stream(self):
        return Stream(self.items())


class query_list(list):
    """
    A list implementation that has the following attributes:
        - query is directly implemented within the object
        - the length of the list can be accessed via list_instance.len as a property
            instead of needing to invoke __length__
    """

    @property
    def len(self):
        return self.__len__()

    def __getitem__(self, item):
        """
        Allows us to execute queries on a dict or list by simply
        adding a '?' before the query when using braces to access
        a member. If a question mark is not present, assume
        that we are attempting to access a member of the dict.

        e.g.: queried_item = dict_instance['?list:0']
        """
        if isinstance(item, str):
            if item.find('?', 0, 1) == 0:
                return self.query(item[1:])

        # otherwise act as normal
        return super().__getitem__(item)

    def query(self, query_string, filters=None):
        """
        Performs a query search with 'query_string' as the search
        string
        :param query_string: Search string to access desired member(s)
        :param filters: Filter methods to perform on the result preceding
        the filter operator
        :return: object(s) if exists, otherwise exception is thrown
        """
        return query_collections.search.query(self, query_string, filters=filters)

    def stream(self):
        return Stream(self)


class Comparators:
    """
    Collection of comparators for use in the stream max/min methods.
    """

    @staticmethod
    def default_max(a, b):
        return a > b

    @staticmethod
    def default_min(a, b):
        return a < b


class Optional:
    """
    Port of the Java Optional class.
    """

    def __init__(self, instance=None):
        self.instance = instance

    def get(self):
        return self.instance

    def ifPresent(self, consumer):
        if self.instance is not None:
            return consumer(self.instance)

    def isPresent(self):
        return self.instance is not None

    def map(self, mapper):
        return Optional(mapper(self.instance))

    def orElse(self, other):
        return self.instance if self.instance is not None else other

    def orElseGet(self, other_fn):
        return self.instance if self.instance is not None else other_fn()

    def orElseThrow(self, exception_class):
        if self.instance is not None:
            return self.instance
        else:
            raise exception_class("Optional did not exist!")

    def __str__(self):
        return "Optional(" + str(self.instance) + ")"


class Stream(list):
    """
    A collection of methods that can be used to perform stream operations
    as made popular by the Java 8 Stream class.
    """

    def __getitem__(self, index):
        if index < self.__len__():
            return super().__getitem__(index)
        else:
            return None

    def allMatch(self, predicate_fn):
        """
        Returns true if every member of this stream returns true
        for predicate_fn(member)
        :param predicate_fn: Method to invoke each member with.
        :return: Boolean
        """
        return all([predicate_fn(member) for member in self])

    def anyMatch(self, predicate_fn):
        """
        Returns true if any member of this stream returns true
        for predicate_fn(member)
        :param predicate_fn: Method to invoke each member with.
        :return: Boolean
        """
        return any([predicate_fn(member) for member in self])

    def concat(self, b):
        """
        Appends the elements of stream b to the elements of a.
        :param b: Stream containing other elements.
        :return:
        """
        if isinstance(b, Stream):
            return self + b
        else:
            raise Exception("Can't concatenate this stream with a non stream type!")

    def length(self):
        """
        Retuns the number of elements in this stream
        """
        return self.__len__()

    def filter(self, filtering_fn):
        """
        Returns a new stream containing elements where filtering_fn(element)
        returns true
        :param filtering_fn: Method to perform filtering
        :return: Stream
        """
        return Stream(filter(filtering_fn, self))

    def findAny(self):
        """
        Return an optional containing random element from this stream,
        should an element exist.
        :return: Optional
        """
        return Optional(random.choice(self))

    def findFirst(self):
        """
        Returns an optional containing the first element of this
        stream, should it exist.
        :return type: Optional
        """
        return Optional(self.__getitem__(0))

    def forEach(self, fn):
        """
        Invokes fn with each member of this stream and returns this steam unmodified
        :param fn: Method to invoke with each member
        :return: This Stream instance
        """
        [fn(member) for member in self]

    def limit(self, maxSize):
        """
        Returns the first N elements of this stream, until maxSize is
        reached or we reach the end of the stream.
        :param maxSize: The max elements to return.
        """
        return itertools.islice(self, 0, stop=maxSize)

    def map(self, mapper):
        """
        Returns a mapped Stream where each element is
        mapped to a new value by mapper
        :param mapper: A lambda expression or method to perform
        the mapping.
        :return: Stream
        """
        return Stream([mapper(item) for item in self])

    def mapToFloat(self):
        """
        Maps each element of this stream to a float
        :return: Stream
        """
        return Stream([float(item) for item in self])

    def matToInt(self):
        """
        Maps each element of this stream to an integer
        :return: Stream
        """
        return Stream([int(item) for item in self])

    def max(self, key=None):
        """
        Returns the max element of this stream
        :param comparator: A comparator to perform the comparison
        to find the max value.
        :return: An optional containing the max value.
        """

        if len(self) == 0:
            return Optional()

        return Optional(max(self, key=key))

    def min(self, key=None):
        """
        Returns the min element of this stream
        :param key: Lambda expression used to perform the minimum operation,
        passed to the builtin 'min' method.
        :return: An optional containing the min value.
        """

        if len(self) == 0:
            return Optional()

        return Optional(min(self, key=key))

    def noneMatch(self, predicate_fn):
        """
        Returns whether or not all element of this Stream
        do not return true by predicate_fn(element)
        :param predicate_fn:
        :return:
        """
        return not all([predicate_fn(item) for item in self])

    def peek(self, action_fn):
        """
        Returns the elements of this stream, additionally performing
        action_fn(element) for each element in this stream.
        :param action_fn: Method to be performed with each element.
        :return: Stream (the same stream)
        """
        [action_fn(item) for item in self]
        return self

    def reduce(self, accumulator):
        """
        Performs a reduction on the elements of this stream.
        :param accumulator: The accumulator method to perform the
        reduction.
        :return: An optional containing the reduced value, should it exist.
        """
        return Optional(reduce(accumulator, self))

    def skip(self, n):
        """
        Returns all elements in this stream after position n
        :param n: Position to start reading elements from.
        :return: Stream
        """
        return Stream(itertools.islice(self, n))

    def sorted(self, **kwargs):
        """
        Sorts this stream.
        :param kwargs: keyword arguments to pass to the native sorted Python
        builtin.
        :return: Stream
        """
        return Stream(sorted(self, **kwargs))

    def sum(self):
        """
        Returns the sum of elements in this list.
        :return: Integer
        """
        return sum(self)

    def as_list(self):
        """
        Returns the elements of this stream as a list of tuples or values
        :return: query_list
        """
        return list(self)

    def as_dict(self):
        """
        Returns a dictionary representing this Stream, where elements
        of this stream are tuples (key, value)
        :return: query_dict
        """
        return query_dict(self)

    @staticmethod
    def concat(a, b):
        """
        Concatenates b to a and returns the concatenation as a stream.
        :param a:
        :param b:
        :return:
        """
        return Stream(a + b)

    @staticmethod
    def empty():
        """
        :return: Stream contaning zero elements
        """
        return Stream()

    @staticmethod
    def generate(iterable):
        """
        Create a stream from an iterable method
        :return: Stream
        """
        return Stream(iterable)

    @staticmethod
    def of(*args):
        """
        Constructs a stream from a list of values
        :param args: Arguments to pack into a stream
        :return: Stream
        """
        return Stream(args)