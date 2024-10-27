import sys
import requests
from time import time
from string import ascii_letters, digits

# Constants
BASE_URL = "https://gpay.app.goo.gl/"

# Predefine target substrings
TARGETS = {
    "share_sheet_item1_v5.png": "Color Laddoo Found",
    "share_sheet_item2_v3.png": "Foodie Laddoo Found",
    "share_sheet_item3_v3.png": "Disco Laddoo Found",
    "share_sheet_item4_v3.png": "Dosti Laddoo Found",
    "share_sheet_item5_v3.png": "Trendy Laddoo Found",
    "share_sheet_item6_v3.png": "Twinkle Laddoo Found"
}

CHARS = ascii_letters + digits  # Characters used in hashes
CHARSET_SIZE = len(CHARS)

last_checked_hash = sys.argv[1] if len(sys.argv) > 1 else 'aaaaaa'

# Convert a hash to an index
def hash_to_index(hash_str):
    index = 0
    for char in hash_str:
        index = index * CHARSET_SIZE + CHARS.index(char)
    return index

# Convert an index back to a hash
def index_to_hash(index, length=6):
    chars = []
    for _ in range(length):
        chars.append(CHARS[index % CHARSET_SIZE])
        index //= CHARSET_SIZE
    return ''.join(reversed(chars))

# Custom generator starting from a specific hash
def generate_combinations(start_hash):
    # Calculate starting index
    start_index = hash_to_index(start_hash)
    while True:
        yield index_to_hash(start_index)
        start_index += 1

# Save found hashes to a separate file for future reference
def save_found_hash(found_hash):
    with open('UsedLinks.txt', "a") as f:
        f.write(BASE_URL+found_hash + "\n")

# Notify function
def ntfy(title, message):
    requests.post("https://ntfy.sh/", json={
        "topic": "i49Y47_Laddoo",
        "message": message,
        "title": title,
        "priority": 5
    })

# Check hash and notify if a target is found
n = 0
def check_hash(hash_suffix):
    global n
    n += 1
    hash_url = f"{BASE_URL}{hash_suffix}"
    res = requests.get(hash_url).text
    
    if "Laddoo for you" in res:
        for target, title in TARGETS.items():
            if target in res:
                ntfy(title, hash_url)
                save_found_hash(hash_suffix)
                return  # Exit early if found
        ntfy("Unknown Laddoo Found", res)
        save_found_hash(hash_suffix)
    
    if n % 100 == 0:
        print(f">>>> {n}: Last Hash - {hash_suffix}, [{n / (time() - start):.2f} HPs]", end='\r')

start = time()

for hash_suffix in generate_combinations(last_checked_hash):
    check_hash(hash_suffix)

print("\nCompleted.")