import os
import hashlib
import json
import time
import configparser
from alert import alert

def compute_hash(file_path):
    """
    Compute SHA256 hash of a file.
    """
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except (OSError, IOError):
        return None

def load_database(db_path):
    """
    Load the hash database from JSON file.
    """
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_database(db_path, db):
    """
    Save the hash database to JSON file.
    """
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=4)

def scan_directory(path):
    """
    Scan the directory and compute hashes for all files.
    """
    files = {}
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            hash_val = compute_hash(full_path)
            if hash_val:
                files[full_path] = hash_val
    return files

def detect_changes(old_db, new_db):
    """
    Detect changed, new, and deleted files.
    """
    changed = []
    new_files = []
    deleted = []
    for path, hash_val in new_db.items():
        if path not in old_db:
            new_files.append(path)
        elif old_db[path] != hash_val:
            changed.append(path)
    for path in old_db:
        if path not in new_db:
            deleted.append(path)
    return changed, new_files, deleted

def detect_mass_renaming(deleted, new_files, new_db, old_db):
    """
    Detect potential mass file renaming.
    Simplistic check: if number of deleted equals number of new files,
    and the set of hashes is the same, likely renaming.
    Requires at least 2 files to avoid false positives from editor temp saves.
    """
    if not deleted or not new_files:
        return False
    if len(deleted) != len(new_files):
        return False
    # Ignore single file operations (likely editor temp saves)
    if len(deleted) < 2:
        return False
    old_hashes = {old_db[path] for path in deleted if path in old_db}
    new_hashes = {new_db[path] for path in new_files if path in new_db}
    return old_hashes == new_hashes

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(script_dir, 'config.ini'))
    monitor_path = os.path.join(script_dir, config['monitor']['path'])
    interval = int(config['monitor'].get('interval', 60))
    db_path = os.path.join(script_dir, 'hash_database.json')

    print("File Integrity Monitor started. Monitoring:", monitor_path)
    print("Press Ctrl+C to stop.")

    while True:
        db = load_database(db_path)
        new_db = scan_directory(monitor_path)
        changed, new_files, deleted = detect_changes(db, new_db)

        if changed:
            alert(f"Sudden changes detected in {len(changed)} files: {changed[:5]}...")  # Show first 5

        if detect_mass_renaming(deleted, new_files, new_db, db):
            alert("Mass file renaming detected!")

        # Update database
        save_database(db_path, new_db)

        time.sleep(interval)

if __name__ == "__main__":
    main()
