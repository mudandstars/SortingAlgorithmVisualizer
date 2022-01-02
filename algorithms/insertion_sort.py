"""
Insertion sort sorts the list in place.
Begins at the left-most element of the list and works itself to the right end.
Sub-divides the list into sorted (left-end) and unsorted (right-end).
Sorts the list in place by inserting the current value in its designated space in the sorted part of the list.
"""


def insertion_sort(object):
    """
    Insertion sort algorithm that is augmented to also visualize the process.
    :param object: Instance of MainScreen class
    :return: List (indices and values of items to draw)
    """
    indices = []
    i = 1
    while i < len(object.items):
        j = i
        while j > 0 and object.items[j - 1] > object.items[j]:

            indices.append((i, j - 1, j, object.items[j - 1], object.items[j]))

            # swap elements if they are not in order
            object.switch_items(j - 1, j)
            # repeat for each element in the sorted list (left part of array)
            j -= 1

        # go one step to the right and repeat
        i += 1

    return indices
