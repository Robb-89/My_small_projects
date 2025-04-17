import json



file_path = r'C:\Users\rober\Downloads\Heap-20250415T155135.heapsnapshot'
def load_heap_snapshot(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return json.load(f)

def get_edge_types(snapshot_data):
    meta = snapshot_data['snapshot']['meta']
    edge_types = meta['edge_types'][0]  # Edge types like 'property', 'element', etc.
    edge_fields = meta['edge_fields']   # Field names like 'type', 'name_or_index', etc.
    
    type_index = edge_fields.index('type')
    edge_type_enum = edge_types
    
    edges = snapshot_data['edges']
    edge_fields_count = len(edge_fields)
    
    unique_types = set()
    
    for i in range(0, len(edges), edge_fields_count):
        type_enum_val = edges[i + type_index]
        edge_type_name = edge_type_enum[type_enum_val]
        unique_types.add(edge_type_name)
    
    return unique_types

if __name__ == '__main__':
    # Replace with your .heapsnapshot file path
    path_to_snapshot = r'C:\Users\rober\Downloads\Heap-20250415T155135.heapsnapshot'



file_path = r'"C:\Users\rober\Downloads\Heap-20250415T155135.heapsnapshot"'
def load_heap_snapshot(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return json.load(f)

def get_edge_types(snapshot_data):
    meta = snapshot_data['snapshot']['meta']
    edge_types = meta['edge_types'][0]  # Edge types like 'property', 'element', etc.
    edge_fields = meta['edge_fields']   # Field names like 'type', 'name_or_index', etc.
    
    type_index = edge_fields.index('type')
    edge_type_enum = edge_types
    
    edges = snapshot_data['edges']
    edge_fields_count = len(edge_fields)
    
    unique_types = set()
    
    for i in range(0, len(edges), edge_fields_count):
        type_enum_val = edges[i + type_index]
        edge_type_name = edge_type_enum[type_enum_val]
        unique_types.add(edge_type_name)
    
    return unique_types

if __name__ == '__main__':
    # Replace with your .heapsnapshot file path
    path_to_snapshot = r'C:\Users\rober\Downloads\Heap-20250415T155135.heapsnapshot'
    snapshot = load_heap_snapshot(path_to_snapshot)
    edge_types = get_edge_types(snapshot)
    
    print("Unique edge types found:")
    for edge_type in sorted(edge_types):
        print(f"- {edge_type}")
    snapshot = load_heap_snapshot(path_to_snapshot)
    edge_types = get_edge_types(snapshot)
    
    print("Unique edge types found:")
    for edge_type in sorted(edge_types):
        print(f"- {edge_type}")
