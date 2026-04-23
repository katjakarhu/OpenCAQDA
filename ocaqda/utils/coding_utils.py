from ocaqda.data.models import CodeRelationship
from ocaqda.utils.codetree import CodeTree


def convert_and_merge_ranges(l):
    from collections import defaultdict

    # Step 1: Create a dictionary to map each point to its labels
    point_to_labels = defaultdict(set)

    for start, end, label in l:
        for point in range(start, end + 1):
            point_to_labels[point].add(label)

    if not point_to_labels:
        return []

    # Step 2: Sort the points
    sorted_points = sorted(point_to_labels.keys())

    # Step 3: Merge consecutive points with the same labels
    result = []
    current_start = sorted_points[0]
    current_labels = point_to_labels[current_start]

    for point in sorted_points[1:]:
        if point_to_labels[point] == current_labels:
            continue
        else:
            # Add the current range to the result
            if len(current_labels) == 1:
                label = next(iter(current_labels))
            else:
                label = current_labels
            result.append([current_start, point - 1, label])
            current_start = point
            current_labels = point_to_labels[point]

    # Add the last range
    if len(current_labels) == 1:
        label = next(iter(current_labels))
    else:
        label = current_labels
    result.append([current_start, sorted_points[-1], label])

    return result


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
            node_map[from_code_id] = CodeTree(from_code[0])
        if to_code_id is not None and to_code_id not in node_map:
            node_map[to_code_id] = CodeTree(to_code[0])

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
