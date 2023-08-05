import query_collections.search


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
