
import pydicom
import sys
import os


def read_dicom(path):
    try:
        ds = pydicom.dcmread(path)
        return ds
    except Exception as e:
        print(f"Error reading the DICOM file: {e}")
        sys.exit(1)


def export_to_txt(ds, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(ds))
        print(f"File successfully exported to: {output_path}")
    except Exception as e:
        print(f"Error exporting the file: {e}")


def main():
    dicom_path = input("Enter the path of the DICOM file: ").strip()
    if not os.path.exists(dicom_path):
        print("Error: The specified path does not exist.")
        sys.exit(1)

    ds = read_dicom(dicom_path)

    export = input("Do you want to export it to a text file? (y/n): ").strip().lower()
    if export == "y":
        output_path = input("Enter the path where you want to save the file: ").strip()
        if not os.path.exists(output_path):
            print("Error: The specified path does not exist.")
            sys.exit(1)
    
        file_name = os.path.basename(dicom_path).replace(".dcm", ".txt")
        full_path = os.path.join(output_path, file_name)
        export_to_txt(ds, full_path)

    display = input("Do you want to display the content on the console? (y/n): ").strip().lower()
    if display == "y":
        print(ds)


if __name__ == "__main__":
    main()