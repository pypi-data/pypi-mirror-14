def eq(compare_item):
    """
    Ensures the filtered item equals the compare_item

    result == compare_item
    :return: Callback to be used by the query search.
    """

    def callback(item):
        return item == compare_item

    return callback


def less(compare_item):
    """
    Ensures the filtered item is less than the compare_item

    result < compare_item
    :return: Callback to be used by the query search.
    """

    def callback(item):
        return item < compare_item

    return callback


def greater(compare_item):
    """
    Ensures the filtered item is greater than the compare_item

    result > compare_item
    :return: Callback to be used by the query search.
    """

    def callback(item):
        return item > compare_item

    return callback


def lessEqual(compare_item):
    """
    Ensures the filtered item is greater than or equal to the compare_item

    result <= compare_item
    :return: Callback to be used by the query search.
    """

    def callback(item):
        return item <= compare_item

    return callback


def greaterEqual(compare_item):
    """
    Ensures the filtered item is greater than or equal to the compare_item

    result >= compare_item
    :return: Callback to be used by the query search.
    """

    def callback(item):
        return item >= compare_item

    return callback
