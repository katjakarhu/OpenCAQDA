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
    overlapped_ranges, not_overlapped_ranges = find_overlap(sorted_ranges)

    # merged_ranges = []
    ##for begin, end, labels in overlapped_ranges:
    #    print(begin, end, labels)
    #    for begin2, end2, labels2 in overlapped_ranges:

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

    print("r", result)

    result = result + not_overlapped_ranges
    merged_ranges = sorted(result, key=lambda x: x[0])

    return merged_ranges


def find_overlap(sorted_ranges):
    overlapped_items = []
    free_items = []

    for i in range(len(sorted_ranges)):
        overlap = False

        # if sorted_ranges[i][0] <= sorted_ranges[j][1]:
        if sorted_ranges[i][1] >= min([sublist[0] for sublist in sorted_ranges]):
            overlap = True
        elif sorted_ranges[i][0] <= max([sublist[1] for sublist in sorted_ranges]):
            overlap = True

        if overlap:
            overlapped_items.append(sorted_ranges[i])
        else:
            free_items.append(sorted_ranges[i])

    print("o:", overlapped_items)
    print("f:", free_items)

    return overlapped_items, free_items


def set_ranges2(sorted_ranges):
    merged_ranges = []

    for begin, end, labels in sorted_ranges:
        if len(merged_ranges) == 0:
            merged_ranges.append([begin, end, labels])
            print("e0")
            continue
        elif end < min([sublist[0] for sublist in merged_ranges]):
            merged_ranges.append([begin, end, labels])
            print("e1")
            continue
        elif begin > max([sublist[1] for sublist in merged_ranges]):
            merged_ranges.append([begin, end, labels])
            print("e2")
            continue
        else:
            j = 0
            x = len(merged_ranges)
            while j < x:
                print("While start ->")
                print(begin, end, labels, merged_ranges[j])
                print("<- while start.")

                merged_item = merged_ranges[j]

                labels_included = contains_labels(labels, merged_item[2]) and contains_labels(merged_item[2], labels)

                if begin == merged_item[0] and end == merged_item[1] and labels == merged_item[2]:
                    print("!!!!")
                    continue
                elif begin > merged_item[0] and end < merged_item[1] and labels_included:
                    print("!!!!?????")
                    continue
                elif begin > merged_item[0] and end < merged_item[1] and not labels_included:
                    print("first")
                    new_set = set()
                    new_set.add(merged_item[2])
                    new_set.add(labels)
                    print([begin, end, new_set])
                    merged_ranges.append([begin, end, new_set])
                    print([end + 1, merged_item[1], merged_item[2]])
                    merged_ranges.append([end + 1, merged_item[1], merged_item[2]])
                    merged_item[1] = begin - 1
                    print(merged_item[1])

                    j += 1

                elif begin == merged_item[0] and end >= merged_item[1] and not labels_included:
                    print("middle")
                    new_set = set()
                    new_set.add(labels)
                    if isinstance(merged_item[2], str):
                        new_set.add(merged_item[2])
                    else:
                        new_set.update(merged_item[2])
                    merged_item[2] = new_set
                    merged_ranges.append([merged_item[1] + 1, end, labels])
                    j += 1

                elif begin <= merged_item[1] and end >= merged_item[1] and not labels_included:
                    print("last")
                    print(begin, end, merged_ranges[j])
                    # [[20, 129, 'Lorem'], [130, 134, {'Lorem', 'Dolor'}], [135, 135, {'Lorem', 'Ipsum', 'Dolor'}], [136, 200, 'Dolor'], [136, 201, 'Ipsum']]
                    # 135 201 [136, 200, 'Dolor']
                    # added [135, 200, {'Dolor', 'Ipsum'}]
                    # added [201, 201, 'Ipsum']
                    # modified end [136, 200, 'Dolor']
                    # [[20, 129, 'Lorem'], [130, 134, {'Dolor', 'Lorem'}], [135, 135, {'Dolor', 'Ipsum', 'Lorem'}], [136, 200, 'Dolor'], [136, 201, 'Ipsum'], [135, 200, {'Dolor', 'Ipsum'}], [201, 201, 'Ipsum']]
                    print(merged_ranges)
                    new_set = set()
                    if isinstance(merged_item[2], str):
                        new_set.add(merged_item[2])
                    else:
                        new_set.update(merged_item[2])
                    new_set.add(labels)
                    print("added", [begin, merged_item[1], new_set])
                    merged_ranges.append([begin, merged_item[1], new_set])
                    print("added", [merged_item[1] + 1, end, labels])
                    merged_ranges.append([merged_item[1] + 1, end, labels])
                    if begin - 1 >= merged_item[0]:
                        merged_item[1] = begin - 1
                    print("modified end", merged_item)
                    # merged_ranges = sorted(merged_ranges, key=lambda x: x[0])
                    print(merged_ranges)

                    j += 1

                # elif begin < merged_item[1] and end >= merged_item[1] and not labels_included:
                else:
                    print("ELSE")
                    print(begin, end, labels, merged_ranges[j])

                merged_ranges = sorted(merged_ranges, key=lambda x: x[0])

                j += 1
                x = len(merged_ranges)
        merged_ranges = sorted(merged_ranges, key=lambda x: x[0])

    print(merged_ranges)
    return merged_ranges


def set_ranges_old(sorted_ranges):
    # Initialize a list to store the merged ranges
    merged_ranges = []

    has_overlap = True

    i = 0

    while i < len(sorted_ranges) - 1:
        s1 = sorted_ranges[i][0]
        e1 = sorted_ranges[i][1]
        l1 = sorted_ranges[i][2]
        s2 = sorted_ranges[i + 1][0]
        e2 = sorted_ranges[i + 1][1]
        l2 = sorted_ranges[i + 1][2]
        print(s1, e1, s2, e2)

        if s1 == s2 and e1 == e2:
            print("duplicate range")
            print(s1, e1)

        # No overlap between the two list entries, let's add both to the result
        # list and move the index over to the next unhandled element
        if e1 < s2:
            if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                merged_ranges.append([s1, e1, l1])
            if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                merged_ranges.append([s2, e2, l2])
            i += 2
            continue

        else:

            if s1 != s2:
                if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                    merged_ranges.append([s1, s2 - 1, l1])

            if e2 < e1:
                if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                    merged_ranges.append([s2, e2, l1 + l2])

                if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                    merged_ranges.append([e2 + 1, e1, l1])
            else:
                if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                    merged_ranges.append([s2, e1, l1 + l2])
                if not contains_range_with_label(sorted_ranges[i], merged_ranges):
                    merged_ranges.append([e1 + 1, e2, l2])

        i = i + 1
    merged_ranges = sorted(merged_ranges, key=lambda x: x[0])
    print(merged_ranges)

    return merged_ranges


def contains_range_with_label(item, merged_ranges):
    if len(merged_ranges) > 0:
        for m in merged_ranges:
            if m[0] <= item[0] and m[1] >= item[1] and item[2] in m[2]:
                return True

    return False
