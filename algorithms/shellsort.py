
def shell_sort(unsorted_list):
    """
    Optimized insertion sort that allows the exchange of items that are far apart.
    Sorts the list in place by iteratively swapping elements, first very far apart and eventually only 1 space apart,
    making it a normal insertion sort at the end.
    :param unsorted_list: list (unsorted list)
    :return: None
    """
    # use Ciura gap sequence
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    # start with largest gap and work down to gap of 1
    for gap in gaps:
        offset = 0
        # offset is iterating through the list by 1 step at a time
        while offset < gap:
            i = offset
            # i is iterating through the list, starting with offset and incremented by the gap-value every iteration
            while i < len(unsorted_list):
                # the current value of list[i] is saved temporarily
                temp = unsorted_list[i]
                j = i
                # j starts at i and decreases by the gap-value each iteration.
                # j serves to shift earlier gap-sorted elements up until the correct location for list[i] is found
                while j >= gap and unsorted_list[j - gap] > temp:
                    unsorted_list[j] = unsorted_list[j - gap]
                    j -= gap

                # put the original list[i] item in its correct location
                unsorted_list[j] = temp
                i += gap
            offset += 1
