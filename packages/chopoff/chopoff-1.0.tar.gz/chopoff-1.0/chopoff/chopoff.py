"""
This module returns the remainder of the slice of an iterable
Usage: chopoff([6, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) -> [1, 2, 3, 4, 5, 6, 9, 10]
"""


def chopoff(list_slice, iterable):
    """
    :param list_slice: A list containing the slices you want to take, if follows the normal order of python slices
    :param iterable: The iterable you want to slice
    :return: The remainder of the given slice
    """

    # if one argument was passed
    if len(list_slice) == 1:
        return iterable[:list_slice[0]]

    # if two arguments were passed
    elif len(list_slice) == 2:
        return iterable[:list_slice[0]] + iterable[list_slice[1]:]

    # if three arguments were passed
    elif len(list_slice) == 3:
        if list_slice[2] < 0 and list_slice[0] <= list_slice[1]:
            return []

        elif list_slice[2] > 0 and list_slice[0] == list_slice[1]:
            return []  # fail silently because a list_slice of [n:n] would not return anything

        else:
            return iterable[:list_slice[0]] + iterable[list_slice[0]+1:list_slice[1]-1:list_slice[2]] + iterable[list_slice[1]:]
    else:
        raise SyntaxError('an iterable list_slice cannot have more than three positions')
