from intervaltree import IntervalTree


def find_range_overlap(a, b):
    ol = range(max(a[0], b[0]), min(a[-1], b[-1]) + 1)
    if len(ol) == 0:
        return None, None
    return ol[0], ol[-1]


def find_overlapping_intervals(intervals):
    tree = IntervalTree()
    for interval in intervals:
        tree[interval[0]:interval[1]] = True
    tree.merge_overlaps()  # Merge overlapping intervals
    return sorted((int(begin), int(end)) for begin, end, _ in tree)


def convert_and_merge_ranges(input_ranges):
    # Sort the ranges based on the start position
    sorted_ranges = sorted(input_ranges, key=lambda x: x[0])

    print(sorted_ranges)

    # while has_overlap:
    #    while i < len(sorted_ranges):
    # s1, e1, labels1 = sorted_ranges[i]

    # Iterate through the sorted ranges

    merged_ranges = set_ranges(sorted_ranges)

    return merged_ranges


def contains_labels(l, labels):
    if isinstance(l, str):
        if isinstance(labels, str):
            return l == labels
        else:
            return l in labels
    else:
        if isinstance(labels, str):
            return False
        else:
            return l.issubset(labels)


def set_ranges(sorted_ranges):
    """
    Note that this method is vibe-coded with Mistral.ai
    """
    # Let's separate the overlapping ranges from non-overlapping ones
    overlapped_ranges, not_overlapped_ranges = find_overlap(sorted_ranges)

    # Initialize a dictionary to hold the merged data
    merged_dict = {}

    # Iterate over each range in the input list
    for start, end, value in overlapped_ranges:
        # Ensure the range is correctly ordered
        low, high = sorted([start, end])

        # For each number in the range, add the value to the dictionary
        for num in range(low, high + 1):
            if num in merged_dict:
                # If the number is already in the dictionary, we need to merge the values
                if isinstance(merged_dict[num], set):
                    print(merged_dict[num])
                    merged_dict[num].add(value)
                else:
                    # Convert the existing value to a set and add the new value
                    merged_dict[num] = {merged_dict[num], value}
            else:
                # If the number is not in the dictionary, add it with the current value
                merged_dict[num] = value

    # Convert the dictionary back to a list of lists and merge consecutive ranges with the same value
    result = []
    if merged_dict:
        start_num = min(merged_dict.keys())
        current_value = merged_dict[start_num]

        for num in range(start_num + 1, max(merged_dict.keys()) + 1):
            if merged_dict.get(num) != current_value:
                result.append([start_num, num - 1, current_value])
                start_num = num
                current_value = merged_dict[num]

        result.append([start_num, max(merged_dict.keys()), current_value])


    result = result + not_overlapped_ranges
    merged_ranges = sorted(result, key=lambda x: x[0])
    print("r", merged_ranges)

    return merged_ranges


def find_overlap(sorted_ranges):
    overlapped_items = []
    free_items = []

    for i in range(len(sorted_ranges)):
        print(i)
        overlap = False

        for j in range(len(sorted_ranges)):
            if j != i:
                if sorted_ranges[j][0] <= sorted_ranges[i][1] and sorted_ranges[j][1] >= sorted_ranges[i][0]:
                    overlap = True

        if overlap:
            overlapped_items.append(sorted_ranges[i])
        else:
            free_items.append(sorted_ranges[i])

    return overlapped_items, free_items

