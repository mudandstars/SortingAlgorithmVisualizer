

def insertion_sort(unsorted_list):
    """
    Insertion sort sorts the list in place.
    Begins at the left-most element of the list and works itself to the right end.
    Sub-divides the list into sorted (left-end) and unsorted (right-end).
    Sorts the list in place by inserting the current value in its designated space in the sorted part of the list.
    :param unsorted_list: list (list to be sorted)
    :return: None
    """
    i = 1
    while i < len(unsorted_list):
        j = i
        while j > 0 and unsorted_list[j - 1] > unsorted_list[j]:
            # swap elements if they are not in order
            store = unsorted_list[j - 1]
            unsorted_list[j - 1] = unsorted_list[j]
            unsorted_list[j] = store

            # repeat for each element in the sorted list (left part of array)
            j -= 1

        # go one step to the right and repeat
        i += 1
