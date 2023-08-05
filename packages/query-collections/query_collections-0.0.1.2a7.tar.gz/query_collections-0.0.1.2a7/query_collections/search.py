import copy
from collections import deque

import query_collections.query_structs
from .exceptions import InvalidQueryException, EmptyQueryException


class NodeType:
    """
    Current implemented query node types.
    BASIC_MEMBER: A key of a component is expected
    WILD_CARD: Any value of parent item is used
    EXIST: If a item exists within it's parent
    """
    BASIC_MEMBER = 0
    WILD_CARD = 1
    EXIST = 2


class QueryNode:
    """
    A node that represents the query for a desired member.
    node_type is a NodeType object that represents the search tyep.
    value is a string representation of the component to search for.
    """
    node_type = None  # NodeType
    value = None

    def __init__(self, search_string):
        node_type = classify(search_string)
        if node_type is NodeType.BASIC_MEMBER:
            self.value = search_string
        elif node_type is NodeType.EXIST:
            self.value = search_string.split('!')[0]
        else:
            self.value = '*'  # NodeType.wildcard
        self.node_type = node_type


def classify(query_component_string):
    """
    Classifies a query component string.
    :param query_component_string: A component of the query to perform the
    classification on
    :return: The NodeType of the string.
    """
    if query_component_string == "*":
        return NodeType.WILD_CARD
    elif query_component_string.find("!") != -1:
        return NodeType.EXIST
    else:
        return NodeType.BASIC_MEMBER


def make_search_queue(query_string):
    """
    Makes the search queue associated with a query string.
    This is used when recursively performing the query on the object.

    :param query_string: String to create stack based on
    :return: collections.deque representing the query
    """
    result = deque()
    query_components = query_string.split(":")
    for query_component in query_components:
        result.append(QueryNode(query_component))
    return result


def query(item, search_string):
    """
    Perform a query on a given 'list' or 'dict' type.
    It returns the to be queried information.
    :param item:
    :param search_string:
    :return: The item to be searched for by the given search string.
    :throws: InvalidQueryException if the query is invalid (syntax error or query is empty)
    """
    if search_string is None or search_string == '':
        raise EmptyQueryException
    search_deque = make_search_queue(search_string)
    return recursive_query_search(item, search_deque)


def recursive_query_search(item, search_deque):
    """
    Recursively performs a query on an object. This is to be used
    in conjunction with 'query', and should not be invoked directly.

    :param item: Object to recursively search
    :param search_deque: A collections.deque object that contains
    the query components.
    :return: The item to be searched for if it exists.
    """
    # base case, our search deque is empty, item is what we wanted
    if not search_deque:
        if isinstance(item, list):
            return query_collections.query_structs.query_list(item)
        elif isinstance(item, dict):
            return query_collections.query_structs.query_dict(item)
        else:
            return item

    # get our query component
    query_component = search_deque.popleft()

    if query_component.node_type == NodeType.BASIC_MEMBER:
        """
        We want to continue searching, if it is the desired member it will
        reach our base case
        """
        return recursive_query_search(Handlers[NodeType.BASIC_MEMBER](item, query_component), search_deque)

    elif query_component.node_type == NodeType.WILD_CARD:
        """
        We want to search each member of the current item with the search_deque
        """
        return Handlers[NodeType.WILD_CARD](item, search_deque)

    elif query_component.node_type == NodeType.EXIST:
        """
        We want to return True if the item exists, otherwise False
        """
        return Handlers[NodeType.EXIST](item, query_component, search_deque)


def handle_basic_member(component, query_component):
    """
    Handles a basic member query, assuming the item is NOT an
    object that is not a list or a map
    :param component: list or map to search
    :param query_component: QueryNode to search for
    :return: value of component if it exists, otherwise throws exception
    """

    # if we receive a tuple, tuple[0] = key, tuple[1] = value
    if isinstance(component, tuple):
        component = component[1]

    if isinstance(component, list):
        try:
            index = int(query_component.value)
        except ValueError:
            raise IndexError("Tried to lookup a non-numeric value member %s in a list!" % query_component.value)

        return component[index]

    elif isinstance(component, dict):
        handle_item = component.get(query_component.value)

        if handle_item is not None:
            return handle_item
        else:
            raise KeyError("Member with name %s was not found!" % query_component.value)

    else:
        raise InvalidQueryException(
            "Attempted to perform a query on member %s which was not a map or a list!" % query_component.value)


def handle_wildcard(component, search_queue):
    """
    If we receive a wildcard we want to search all possible members of the
    inputted 'dict' or 'list' object. If it does not exist, it will return an empty list.
    Note: The wildcard silences all exceptions thrown by a query AFTER the wildcard, this is
    intended and should be handled appropriately. Consider an empty result as a sign that
    the component did not exist.

    :param component: object to search through
    :param search_queue: search deque to perform search with
    :return: [object] if the queried item is a list of objects
            object if it is not a list of objects
    """

    # if there is no search deque, this must have been reached
    # where we want all children of a specified condition
    if not search_queue:
        return component

    results = []

    if isinstance(component, list):
        """
        If we are a list, we want to perform the search on
        each item of the inputted component and return the
        matches
        """
        item_list = component

    elif isinstance(component, dict):
        """
        If we are a map, we want to perform the search on
        each value in our key,value map and return the matches
        """
        item_list = component.items()
    else:
        if search_queue:
            raise InvalidQueryException(
                "Attempted to search for member %s, but the parent was not a dict or a list!" % search_queue.popleft().value
            )
        else:
            """
            If we do not have a search deque, this item is the wildcard
            member of the parent component, and is what was wanted.
            (e.g.: dict_instance.query("*") returns the dict_instance)
            """
            return component

    for item in item_list:
        try:
            result = recursive_query_search(item, copy.copy(search_queue))
            results.append(result)
        except:
            """
            If the item did not have a query matching value,
            skip it.
            """
            continue

    return query_collections.query_structs.query_list(results)


def exists(component, query_component):
    try:
        handle_basic_member(component, query_component)
        return True
    except:
        return False


def handle_exist(item, query_component, search_queue):
    """
    Checks if a queried component exists. If there is a search queue,
    it means we will continue to recursively search for underlying members should it exist,
    otherwise not. This case is encountered with the wildcard operator.

    :param item: Item to check if the queried item exists within
    :param query_component: QueryNode that describes the desired member
    :param search_queue: Double ended queue of QueryNode's to continue recursively searching if the
    member exists.
    :return: If a search queue is not present: True or False denoting the existence of the
    component described by in query_component within the item.
            If a search queue is present: Will return the result of performing a recursive search
            on item[query_component] if query_component exists within item, otherwise it will throw
            an exception.
    """
    if search_queue:
        if exists(item, query_component):
            return recursive_query_search(item, search_queue)
        else:
            raise InvalidQueryException("Attempted to search for a value after %s, but %s did not exist" % (
                query_component.value, query_component.value))
    else:
        return exists(item, query_component)


Handlers = {
    NodeType.BASIC_MEMBER: handle_basic_member,
    NodeType.WILD_CARD: handle_wildcard,
    NodeType.EXIST: handle_exist
}
