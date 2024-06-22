import os
import hashlib

def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """calculate the hash of a file using a specified hash algorithm."""
    try:
        hash_func = hashlib.new(hash_algorithm) # to swap between hashes
        with open(file_path, "rb") as f:
            # read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        print(f"Error calculating hash for file {file_path}: {e}")
    return None

def calculate_hashes_in_directory(directory):
    """Calculate hashes for all files in a directory using all available hash algorithms."""
    hash_algorithms = hashlib.algorithms_available
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            for hash_algo in hash_algorithms:
                file_hash = calculate_file_hash(file_path, hash_algo)
                if file_hash:
                    if file_path not in file_hashes:
                        file_hashes[file_path] = {}
                    file_hashes[file_path][hash_algo] = file_hash
    return file_hashes

# Example usage:
folder_path = input("Enter the folder path: ")  # Replace with the path to your folder

file_hashes = calculate_hashes_in_directory(folder_path)

# write hashes to an output file
output_file = "hashes_output.txt"
with open(output_file, "w") as f:
    for file_path, hash_dict in file_hashes.items():
        f.write(f"File: {file_path}\n")
        for hash_algo, file_hash in hash_dict.items():
            f.write(f"\t{hash_algo}: {file_hash}\n")
        f.write("\n")
        f.write("\n")

print(f"Hashes calculated and saved to {output_file}")
