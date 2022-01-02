"""
Heapsort sorts a list by repeatedly splitting it until the list has only one element.
Then it proceeds to merge the lists together in a new list which is returned after all values are merged back.
"""
indices = []


def call_merge_sort(unsorted_list):
    """
    Calls the merge-sort function and returns the drawing-indices and the sorted list.
    This is needed to be able to return properly when using recursive functions here.
    :param unsorted_list: List (unsorted items)
    :return: List, List (tuples of indices for drawing, sorted list of items)
    """
    # the function sorts the list as intended, but I can't figure out a way to pass the correct indices...
    merge_sort(unsorted_list)
    return indices, unsorted_list


def merge_sort(unsorted_list):
    """
    Merge-Sort algorithm that is augmented to enable the drawing process.
    The function sorts the list as intended, but I can't figure out a way to pass the correct indices...
    :return: List (indices and values of items to draw)
    """
    if len(unsorted_list) <= 1:
        return unsorted_list

    else:
        midpoint = len(unsorted_list) // 2
        left_half = unsorted_list[:midpoint]
        right_half = unsorted_list[midpoint:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):

            # swap values if they are in the wrong order
            if left_half[i] < right_half[j]:
                # indices.append(((start_value, end_value of compartment), old_ind, new_ind, old_val, new_val))
                # I don't know how
                unsorted_list[k] = left_half[i]
                i += 1
            else:
                # indices.append(((start_value, end_value of compartment), old_ind, new_ind, old_val, new_val))
                # I don't know how
                unsorted_list[k] = right_half[j]
                j += 1
            k += 1

        # checking if any element was left
        while i < len(left_half):
            unsorted_list[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            unsorted_list[k] = right_half[j]
            j += 1
            k += 1
