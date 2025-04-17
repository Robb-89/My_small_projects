import json

# Config
heap_file = r"C:\Users\rober\Downloads\Heap-20250415T155135.heapsnapshot"

with open(heap_file, "r") as f:
    heap = json.load(f)

# Explore the data structure
print("Keys:", heap.keys())
print("Node count:",len(heap.get("nodes", [])))
print("String count:",len(heap.get("strings", [])))
