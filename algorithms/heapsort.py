"""
Heapsort sorts a list by subdividing it into an unsorted and a sorted region. The former region is a heap and
shrinks iteratively by having its root removed and inserted at the start of the sorted region.
This is sort of an improved selection sort in so far as it finds the largest element more quickly in each step.
"""

import heapq


def heapsort(object):
    """
    Heapsort algorithm augmented to also visualize the process.
    :return: List (indices and values of items to draw)
    """
    heapq._heapify_max(object.items)
    count = 0
    length = len(object.items)
    object.heap_history = []
    indices = []
    new_ind = length - 1
    object.is_heap_sort = True

    while count < length:
        count += 1
        list_subdivision = length - count

        unsorted_part = object.items[:list_subdivision + 1]
        object.heap_history.append(unsorted_part)
        indices.append((list_subdivision, 0, list_subdivision, object.items[0], object.items[list_subdivision]))

        # remove the biggest value and insert it at after the end of the unsorted part of the list
        root = object.items.pop(0)
        object.items.insert(new_ind, root)

        # subdivide list and and restore heap property of unsorted part before merging the lists back together
        unsorted_part = object.items[:list_subdivision]
        sorted_part = object.items[list_subdivision:]
        heapq._heapify_max(unsorted_part)
        unsorted_part.extend(sorted_part)
        object.items = unsorted_part
        new_ind -= 1

    return indices
