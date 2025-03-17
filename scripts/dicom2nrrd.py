
import os
import subprocess
import SimpleITK as sitk
import numpy as np
import pydicom


def create_directory(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def is_segmentation_dicom(dicom_path):
    """Checks if a DICOM file is a valid segmentation."""
    try:
        return pydicom.dcmread(dicom_path).Modality == "SEG"
    except Exception:
        return False


def process_ct(ct_dir, output_path):
    """Converts the CT folder to NRRD using plastimatch."""
    print("Processing CT images...")
    try:
        subprocess.run([
            "plastimatch", "convert", "--input", ct_dir,
            "--output-img", output_path, "--output-type", "float"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    [√] CT converted --> {os.path.normpath(output_path).replace(os.sep, '/')}" )
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [X] Error processing CT: {e}")
        return False


def process_segmentation(seg_dir, ct_output_path, seg_output_path):
    """Processes and resamples the DICOM segmentation."""
    print("Processing segmentation images...")
    seg_files = [os.path.join(seg_dir, f) for f in os.listdir(seg_dir) if f.endswith(".dcm")]
    valid_seg_files = [f for f in seg_files if is_segmentation_dicom(f)]

    if not valid_seg_files:
        print(f"    [X] No valid DICOM segmentation files found in {seg_dir}")
        return False

    seg_file = valid_seg_files[0]
    try:
        seg_image = sitk.ReadImage(seg_file)
        seg_image = sitk.Cast(seg_image, sitk.sitkUInt8)
        seg_array = sitk.GetArrayFromImage(seg_image)
        seg_array[seg_array > 0] = 1
        seg_image = sitk.GetImageFromArray(seg_array)

        ct_image = sitk.ReadImage(ct_output_path)
        seg_image.SetOrigin(ct_image.GetOrigin())
        seg_image.SetDirection(ct_image.GetDirection())
        seg_image.SetSpacing(ct_image.GetSpacing())

        resampled_seg_image = sitk.Resample(
            seg_image, ct_image, sitk.Transform(), sitk.sitkNearestNeighbor, 0, sitk.sitkUInt8)
        seg_resampled_array = sitk.GetArrayFromImage(resampled_seg_image)

        if np.sum(seg_resampled_array) == 0:
            print("    [!] SEG mask is empty after resampling.")
        else:
            sitk.WriteImage(resampled_seg_image, seg_output_path)
            print(f"    [√] SEG converted and resampled --> {os.path.normpath(seg_output_path).replace(os.sep, '/')}" )
        return True
    except Exception as e:
        print(f"    [X] Error processing SEG: {e}")
        return False


def process_single_case():
    """Function to process a single patient."""
    ct_dir = input("Enter the path to the folder containing the DICOM CT image files: ").strip()
    seg_dir = input("Enter the path to the folder containing the DICOM segmentation image: ").strip()
    output_base_dir = input("Enter the path where you want to save the conversion: ").strip()
    output_folder_name = input("Enter the name of the output folder: ").strip()

    output_dir = os.path.join(output_base_dir, output_folder_name)
    create_directory(output_dir)

    ct_output_path = os.path.normpath(os.path.join(output_dir, f"{output_folder_name}_CT.nrrd")).replace(os.sep, '/')
    seg_output_path = os.path.normpath(os.path.join(output_dir, f"{output_folder_name}_SEG_MASK.nrrd")).replace(os.sep, '/')

    if process_ct(ct_dir, ct_output_path):
        process_segmentation(seg_dir, ct_output_path, seg_output_path)

    print("\n-------------------------------------- Process completed --------------------------------------\n")


def process_multiple_cases():
    """Function to process multiple patients."""
    print("\nNames might differ, but the script expects the following folder structure:")
    print("""
    CASES/
    │── PATIENT_1/
    │   │── CT/
    │   │   │── img1.dcm
    │   │   │── ...
    │   │── SEG/
    │   │   │── seg.dcm
    │── PATIENT_2/
    │   │── CT/
    │   │   │── img1.dcm
    │   │   │── ...
    │   │── SEG/
    │   │   │── seg.dcm
    ...
    """)

    root_dir = input("Enter the path to the root folder containing the cases: ").strip()
    output_base_dir = input("Enter the output path for the converted files: ").strip()

    if not os.path.isdir(root_dir):
        print("The entered path is not valid. Exiting...")
        return

    patients = sorted([os.path.join(root_dir, p) for p in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, p))])
    if not patients:
        print("\nNo patient folders found. Exiting...")
        return

    for patient_path in patients:
        print(f"\nProcessing patient: {os.path.basename(patient_path)}")
        sub_dirs = sorted([os.path.join(patient_path, d) for d in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path, d))])

        if len(sub_dirs) < 2:
            print(f"    [X] Not enough folders found in {patient_path}. Skipping.")
            continue

        ct_dir, seg_dir = sub_dirs[:2]
        print(f"    CT detected in: {ct_dir}")
        print(f"    SEG detected in: {seg_dir}")

        output_dir = os.path.join(output_base_dir, os.path.basename(patient_path))
        create_directory(output_dir)

        ct_output_path = os.path.normpath(os.path.join(output_dir, f"{os.path.basename(patient_path)}_CT.nrrd")).replace(os.sep, '/')
        seg_output_path = os.path.normpath(os.path.join(output_dir, f"{os.path.basename(patient_path)}_SEG_MASK.nrrd")).replace(os.sep, '/')

        if process_ct(ct_dir, ct_output_path):
            process_segmentation(seg_dir, ct_output_path, seg_output_path)

    print("\n-------------------------------------- Process completed --------------------------------------\n")


def main():
    num_cases = int(input("Enter the number of cases to convert: ").strip())
    if num_cases == 1:
        process_single_case()
    elif num_cases > 1:
        process_multiple_cases()
    else:
        print("Invalid input. Exiting...")


if __name__ == "__main__":
    main()
