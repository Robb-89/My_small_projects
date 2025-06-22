import json
import re
import sys
import pandas as pd  # ✅ new
from termcolor import colored

# === CONFIG ===
HEAP_FILE = r"C:\Users\rober\OneDrive\Documents\my_scripts\Heap-20250409T213907.heapsnapshot"

KEYWORDS = ["token", "apikey", "Authorization", "bearer", "password"]
PATTERNS = [
    r'ghp_[A-Za-z0-9]{36}',
    r'AIza[0-9A-Za-z\-_]{35}',
    r'Bearer\s+[A-Za-z0-9\-_\.]+',
    r'[A-Za-z0-9_\-]{32,}',
    r'eyJ[A-Za-z0-9\-_]{10,}',
]

# === FUNCTIONS ===
def load_heap_snapshot(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(colored(f"[!] Error loading heap snapshot: {e}", "red"))
        sys.exit(1)

def extract_strings(snapshot):
    return snapshot.get("strings", [])

def find_interesting_strings(strings, keywords, patterns):
    matches = set()
    for s in strings:
        for keyword in keywords:
            if keyword.lower() in s.lower():
                matches.add(s)
        for pattern in patterns:
            if re.search(pattern, s):
                matches.add(s)
    return sorted(matches)

# === MAIN ===
def main():
    print(colored(f"[*] Loading heap snapshot: {HEAP_FILE}", "cyan"))
    snapshot = load_heap_snapshot(HEAP_FILE)

    print(colored("[*] Extracting strings from heap...", "cyan"))
    strings = extract_strings(snapshot)

    print(colored(f"[*] Searching for keywords and patterns...", "cyan"))
    matches = find_interesting_strings(strings, KEYWORDS, PATTERNS)

    if matches:
        print(colored(f"\n[+] Found {len(matches)} interesting strings:\n", "green"))
        for match in matches:
            print(colored(f"  - {match}", "yellow"))
        
        # Save to .txt
        with open("heap_matches.txt", "w", encoding="utf-8") as f:
            for match in matches:
                f.write(match + "\n")
        print(colored("[+] Results saved to heap_matches.txt", "green"))

        # ✅ Save to .csv with pandas
        df = pd.DataFrame(matches, columns=["Matched Strings"])
        df.to_csv("heap_matches.csv", index=False)
        print(colored("[+] Results saved to heap_matches.csv", "green"))

    else:
        print(colored("\n[-] No interesting strings found.", "yellow"))

if __name__ == "__main__":
    main()
