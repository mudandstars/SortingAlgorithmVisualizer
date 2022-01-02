"""
Quicksort sorts the list in place by choosing a pivot value and using pointers starting at the start and end of
the (sub-) list(s). If pointers crossed, return new pivot value and recursively repeat this process until the
list is sorted.
The Hoare partition-scheme chooses the midpoint of the given range as pivot and uses the first and second pointers
to execute the scheme.
"""
indices = []


def quick_sort(unsorted_list, start_index=0, end_index=-1):
    """
    Quicksort algorithm augmented to also visualize the process.
    :param unsorted_list: List (unsorted items)
    :param start_index: int (start index for quicksort)
    :param end_index: int (end index for quicksort)
    :return: List (indices and values of items to draw)
    """
    global indices

    # recursively loop as long as the target range was not worked through yet
    if end_index == -1:
        end_index = len(unsorted_list) - 1
    # recursively loop as long as the target range was not worked through yet
    if start_index < end_index:
        pivot = partition(unsorted_list, start_index, end_index)
        quick_sort(unsorted_list, start_index, pivot)
        quick_sort(unsorted_list, pivot + 1, end_index)

    return indices


def partition(unsorted_list, first_pointer, second_pointer):
    """
    Chooses the midpoint of the given range as pivot and uses the first and second pointers to execute
    the Hoare-partitiion scheme.
    Used by the quicksort function.
    :param unsorted_list: list
    :param first_pointer: int (beginning of sublist)
    :param second_pointer: int (end of sublist)
    :return: int (new pivot index)
    """
    global indices
    middle_of_list = (first_pointer + second_pointer) // 2
    pivot = unsorted_list[middle_of_list]

    # left and right indices
    i = first_pointer
    j = second_pointer

    while True:

        while unsorted_list[i] < pivot:
            i += 1
        while unsorted_list[j] > pivot:
            j -= 1

        # if indices crossed, return pivot
        if i >= j:
            return j

        # if indices have not crossed yet, swap elements
        else:
            indices.append((middle_of_list, i, j, unsorted_list[i], unsorted_list[j]))
            store = unsorted_list[i]
            unsorted_list[i] = unsorted_list[j]
            unsorted_list[j] = store
            i += 1
            j -= 1
