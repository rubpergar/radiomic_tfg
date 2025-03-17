
import os
import csv
import logging
from radiomics import featureextractor


logging.getLogger('radiomics').setLevel(logging.ERROR)


def extract_radiomics_features(image_path, mask_path):
    extractor = featureextractor.RadiomicsFeatureExtractor()
    features = extractor.execute(image_path, mask_path)
    return {k: v for k, v in features.items() if 'diagnostics' not in k}


def save_features_to_csv(features, output_path):
    with open(output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in features.items():
            writer.writerow([key, value])
        print(f"    [√] Radiomics extracted --> {os.path.normpath(output_path).replace(os.sep, '/')}" )


def process_single_patient():
    print("\nRoot pacient folder must contain both CT and SEG nrrd files.")
    root_folder = input("Enter the root folder path containing the CT and SEG files: ")
    patient_name = os.path.basename(os.path.normpath(root_folder))

    print("\nDo you want to save the results?")
    print("\nIf you select 'yes', the extracted radiomic features will be saved in a CSV file inside the same folder.")
    print("If you select 'no', the features will simply be displayed in the console.\n")

    while True:
        save_option = input("(yes/no): ").strip().lower()
        if save_option in ['yes', 'no']:
            break
        print("Invalid input. Please enter 'yes', or 'no'.")

    image_path = os.path.join(root_folder, f"{patient_name}_CT.nrrd")
    mask_path = os.path.join(root_folder, f"{patient_name}_SEG_MASK.nrrd")

    if not os.path.exists(image_path) or not os.path.exists(mask_path):
        print("Error: Image or mask file not found.")
        return

    features = extract_radiomics_features(image_path, mask_path)

    if save_option == 'yes':
        output_csv_path = os.path.join(root_folder, f"{patient_name}_radiomics.csv")
        save_features_to_csv(features, output_csv_path)
    elif save_option == 'no':
        for key, value in features.items():
            print(f"{key}: {value}")
        print("\n-------------------------------------- Process completed --------------------------------------\n")


def process_multiple_patients():
    print("\nPacient folder must contain both CT and SEG nrrd files.")
    root_folder = input("Enter the root folder path containing multiple patient folders: ")

    if not os.path.isdir(root_folder):
        print("Error: Provided path is not a directory.")
        return

    for patient_name in os.listdir(root_folder):
        patient_folder = os.path.join(root_folder, patient_name)
        if os.path.isdir(patient_folder):
            image_path = os.path.join(patient_folder, f"{patient_name}_CT.nrrd")
            mask_path = os.path.join(patient_folder, f"{patient_name}_SEG_MASK.nrrd")

            if os.path.exists(image_path) and os.path.exists(mask_path):
                print(f"\nProcessing patient: {patient_name}")
                features = extract_radiomics_features(image_path, mask_path)
                output_csv_path = os.path.join(patient_folder, f"{patient_name}_radiomics.csv")
                save_features_to_csv(features, output_csv_path)
            else:
                print(f"Skipping {patient_name}: Missing CT or SEG file.")


def main():
    while True:
        try:
            num_patients = int(input("Enter the number of cases to process: "))
            if num_patients >= 1:
                break
            print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Error: Please enter a valid integer.")

    if num_patients == 1:
        process_single_patient()
        print("\n-------------------------------------- Process completed --------------------------------------\n")
    else:
        process_multiple_patients()
        print("\n-------------------------------------- Process completed --------------------------------------\n")


if __name__ == "__main__":
    main()
