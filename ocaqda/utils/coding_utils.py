from ocaqda.data.models import CodeRelationship
from ocaqda.utils.tree import Tree


def convert_and_merge_ranges(input_ranges):
    # Sort the ranges based on the start position
    sorted_ranges = sorted(input_ranges, key=lambda x: x[0])

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

    # Add not overlapping ranges back to the mix and sort
    result = result + not_overlapped_ranges
    merged_ranges = sorted(result, key=lambda x: x[0])

    return merged_ranges


def find_overlap(sorted_ranges):
    overlapped_items = []
    free_items = []

    for i in range(len(sorted_ranges)):
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


def build_tree(relationships, codes):
    """
    Note that this method is vibe-coded with Mistral.ai
    """
    # Create a dictionary to map code_id to TreeNode
    node_map = {}

    # Create TreeNodes for each unique code_id
    for record in relationships:
        from_code_id = record.from_code_id
        to_code_id = record.to_code_id
        from_code = list(filter(lambda x: x.code_id == from_code_id, codes))
        to_code = list(filter(lambda x: x.code_id == to_code_id, codes))
        if from_code_id not in node_map:
            node_map[from_code_id] = Tree(from_code_id, from_code[0].name)
        if to_code_id is not None and to_code_id not in node_map:
            node_map[to_code_id] = Tree(to_code_id, to_code[0].name)

    # Build the tree structure
    for record in relationships:
        from_code_id = record.from_code_id
        to_code_id = record.to_code_id
        parent_node = node_map[from_code_id]
        if to_code_id is not None:
            child_node = node_map[to_code_id]
            parent_node.add_child(child_node)

    # Find and return the root nodes (nodes with no parents)
    all_nodes = set(node_map.keys())
    child_nodes = {r.to_code_id for r in relationships}
    root_nodes = all_nodes - child_nodes

    return [node_map[root_id] for root_id in root_nodes]


def create_tree(code_relationships, codes):
    """Add parents without children to code relationship list and build the tree"""

    # Ids that have parent-child relationships
    ids = []
    for cr in code_relationships:
        ids.append(cr.from_code_id)
        ids.append(cr.to_code_id)

    # Add parents without children to code_relationship
    for code in codes:
        if code.code_id not in ids:
            nr = CodeRelationship()
            nr.from_code_id = code.code_id
            code_relationships.append(nr)

    tree = build_tree(code_relationships, codes)
    return tree
