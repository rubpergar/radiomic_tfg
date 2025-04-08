
import csv


def calculate_variation(value1, value2):
    try:
        num1 = float(value1)
        num2 = float(value2)
        if num1 == 0:
            return "Undefined (division by zero)", None
        variation = abs(((num2 - num1) / abs(num1)) * 100)
        return f"{variation:.15f}%", variation
    except ValueError:
        return "Text or header", None


def compare_csv_files(file1, file2):
    differences = []
    variation_values = []

    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)

            for i, (row1, row2) in enumerate(zip(reader1, reader2), start=1):
                if len(row1) > 0 and len(row2) > 0 and row1[0] == 'diagnostics_Image-original_Hash':
                    continue

                if row1 != row2:
                    variations = []
                    for v1, v2 in zip(row1, row2):
                        variation_str, variation_num = calculate_variation(v1, v2)
                        variations.append(variation_str)
                        if variation_num is not None:
                            variation_values.append(variation_num)
                    differences.append((i, row1, row2, variations))

        if differences:
            print("Differences found:")
            for diff in differences:
                line_num, row1, row2, variations = diff
                print(f"Line {line_num}:")
                print(f"  File 1: {row1}")
                print(f"  File 2: {row2}")
                print(f"  Variation: {variations}")

            avg_variation = sum(variation_values) / len(variation_values) if variation_values else 0
            print(f"\nThe files are different. There are {len(differences)} differences between the files.")
            print(f"Average variation between different values: {avg_variation:.15f}%\n")
        else:
            print("The files are identical.")
    except Exception as e:
        print(f"Error comparing files: {e}")


def main():
    file_path1 = input("Enter the path for the first CSV file: ")
    file_path2 = input("Enter the path for the second CSV file: ")

    compare_csv_files(file_path1, file_path2)


if __name__ == "__main__":
    main()
