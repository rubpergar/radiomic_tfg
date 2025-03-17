
import nrrd
import numpy as np
import os


def compare_nrrd_files(file1, file2):
    try:
        # Load .nrrd files
        data1, header1 = nrrd.read(file1)
        data2, header2 = nrrd.read(file2)

        # Compare data
        data_equal = np.array_equal(data1, data2)

        # Normalize headers for comparison
        def normalize_header(header):
            return {k: str(v) for k, v in header.items() if k not in ['modification_time']}

        header1_normalized = normalize_header(header1)
        header2_normalized = normalize_header(header2)

        # Compare normalized headers
        header_equal = header1_normalized == header2_normalized

        # Print differences if any
        if not header_equal:
            print("Header differences:\n")
            for key in set(header1_normalized.keys()).union(header2_normalized.keys()):
                val1 = header1_normalized.get(key, "Not in header1")
                val2 = header2_normalized.get(key, "Not in header2")
                if val1 != val2:
                    print(f"{key}: {val1} != {val2}")

        if not data_equal:
            print("Data differences: The data arrays are not identical.")

        return data_equal and header_equal
    except Exception as e:
        print(f"Error comparing files: {e}")
        return False


def get_valid_nrrd_path(prompt):
    while True:
        file_path = input(prompt).strip()
        if not os.path.exists(file_path):
            print("Error: The specified path does not exist. Please enter a valid path.")
            continue
        if not file_path.lower().endswith(".nrrd"):
            print("Error: The file is not an NRRD file. Please enter a valid .nrrd file.")
            continue
        return file_path


def main():
    file_path1 = get_valid_nrrd_path("Enter the path of the first NRRD file: ")
    file_path2 = get_valid_nrrd_path("Enter the path of the second NRRD file: ")

    if compare_nrrd_files(file_path1, file_path2):
        print("\n----------------------------- The files are identical -----------------------------\n")
    else:
        print("\n----------------------------- The files are different -----------------------------\n")


if __name__ == "__main__":
    main()
