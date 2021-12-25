
def selection_sort(unsorted_list):
    """
    Sorts list in place.
    Begins at left-most element of the array and works itself to the right end.
    Sub-divides list into sorted (left-end) and unsorted (right-end).
    Scans the list and puts smallest element at the end of the sorted list.
    :param unsorted_list: list (list to be sorted)
    :return: None
    """
    start_unsorted = 0

    while start_unsorted != len(unsorted_list):
        smallest_element = math.inf
        for i in range(start_unsorted, len(unsorted_list)):
            if unsorted_list[i] < smallest_element:
                smallest_element = element

        unsorted_list[start_unsorted] = smallest_element
        start_unsorted += 1
