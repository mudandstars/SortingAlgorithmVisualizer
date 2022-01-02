"""
Sorts list in place.
Begins at left-most element of the array and works itobject to the right end.
Sub-divides list into sorted (left-end) and unsorted (right-end).
Scans the list and puts smallest element at the end of the sorted list.
"""
import math


def selection_sort(object):
    """
    Selection sort algorithm that is augmented to also visualize the process.
    :param object: Instance of MainScreen class
    :return: List (indices and values of items to draw)
    """
    start_unsorted = 0
    indices = []

    while start_unsorted < len(object.items):
        smallest_element = object.items[start_unsorted]
        for i in range(start_unsorted + 1, len(object.items)):
            if object.items[i] < smallest_element:
                indices.append((start_unsorted, start_unsorted, i, object.items[start_unsorted], object.items[i]))
                smallest_element = object.items[i]
                object.items[i] = object.items[start_unsorted]
                object.items[start_unsorted] = smallest_element

        start_unsorted += 1

    return indices
