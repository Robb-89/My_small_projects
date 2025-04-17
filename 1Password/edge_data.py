import json

# List of sensitive keywords to search for
KEYWORDS = ["token", "password", "secret", "auth", "apikey", "authorization"]

def load_heap_snapshot(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return json.load(f)

def resolve_node_value(snapshot_data, to_node_index):
    meta = snapshot_data['snapshot']['meta']
    strings = snapshot_data['strings']
    edges = snapshot_data['edges']
    nodes = snapshot_data['nodes']

    edge_fields = meta['edge_fields']
    node_fields = meta['node_fields']
    node_types = meta['node_types'][0]

    edge_field_count = len(edge_fields)
    node_field_count = len(node_fields)

    node_type_idx = node_fields.index("type")
    node_name_idx = node_fields.index("name")

    edge_name_idx = edge_fields.index("name_or_index")
    edge_to_node_idx = edge_fields.index("to_node")

    node_slice = nodes[to_node_index:to_node_index + node_field_count]
    if len(node_slice) < node_field_count:
        return "<invalid node>"

    node_type_enum = node_slice[node_type_idx]
    node_type = node_types[node_type_enum]
    node_name_index = node_slice[node_name_idx]

    if node_type == "string":
        return strings[node_name_index]

    if node_type == "object":
        result = {}
        for i in range(0, len(edges), edge_field_count):
            from_node = edges[i + edge_to_node_idx]
            if from_node != to_node_index:
                continue

            edge_name_index = edges[i + edge_name_idx]
            prop_name = strings[edge_name_index] if edge_name_index < len(strings) else "<unknown>"

            sub_node_index = edges[i + edge_to_node_idx]
            sub_node = nodes[sub_node_index:sub_node_index + node_field_count]
            if len(sub_node) >= node_field_count:
                sub_type_enum = sub_node[node_type_idx]
                sub_type = node_types[sub_type_enum]
                sub_name_index = sub_node[node_name_idx]
                sub_value = strings[sub_name_index] if sub_type == "string" else f"<{sub_type}>"
                result[prop_name] = sub_value

        return result if result else "<empty object>"

    return f"<non-string node: {node_type}>"

def hunt_sensitive_edges(snapshot_data):
    meta = snapshot_data['snapshot']['meta']
    strings = snapshot_data['strings']
    edges = snapshot_data['edges']
    nodes = snapshot_data['nodes']
    
    edge_fields = meta['edge_fields']
    node_fields = meta['node_fields']
    edge_types = meta['edge_types'][0]
    node_types = meta['node_types'][0]

    edge_field_count = len(edge_fields)
    node_field_count = len(node_fields)

    edge_type_idx = edge_fields.index("type")
    edge_name_idx = edge_fields.index("name_or_index")
    edge_to_node_idx = edge_fields.index("to_node")
    
    node_type_idx = node_fields.index("type")
    node_name_idx = node_fields.index("name")

    print("=== HUNTING FOR SENSITIVE EDGES ===\n")

    for i in range(0, len(edges), edge_field_count):
        edge_type_enum = edges[i + edge_type_idx]
        edge_name_index = edges[i + edge_name_idx]
        edge_to_node_index = edges[i + edge_to_node_idx]

        edge_type = edge_types[edge_type_enum]
        if edge_type != "property":
            continue

        prop_name = strings[edge_name_index]
        if any(keyword in prop_name.lower() for keyword in KEYWORDS):
            print(f"[!] Suspicious property: '{prop_name}'")

            target_node_offset = edge_to_node_index
            node_slice = nodes[target_node_offset:target_node_offset + node_field_count]
            if len(node_slice) < node_field_count:
                print("    [X] Target node out of bounds.")
                continue

            node_type_enum = node_slice[node_type_idx]
            node_type = node_types[node_type_enum]
            node_name_index = node_slice[node_name_idx]
            node_name = strings[node_name_index] if node_name_index < len(strings) else "<unknown>"

            print(f"    → Node type     : {node_type}")
           
