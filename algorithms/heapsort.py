
import heapq


def heapsort(unsorted_list):
    """
    Heapsort sorts a list by subdividing it into an unsorted and a sorted region. The former region is a heap and
    shrinks iteratively by having its root removed and inserted at the start of the sorted region.
    This is sort of an improved selection sort in so far as it finds the largest element more quickly in each step.
    :param unsorted_list: list (list to be sorted)
    :return: None
    """
    heapq._heapify_max(unsorted_list)
    count = 0
    length = len(unsorted_list)

    while count < length:
        count += 1

        # remove the biggest value and insert it at after the end of the unsorted part of the list
        root = unsorted_list.pop(0)
        unsorted_list.insert(-count + 1, root) if count > 1 else unsorted_list.append(root)

        # subdivide list and and restore heap property of unsorted part before merging the lists back together
        list_subdivision = length - count
        unsorted_part = unsorted_list[:list_subdivision]
        sorted_part = unsorted_list[list_subdivision:]
        heapq._heapify_max(unsorted_part)
        unsorted_part.extend(sorted_part)
        unsorted_list = unsorted_part
