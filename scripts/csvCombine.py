import os
import pandas as pd


def read_csvs_from_folder(root_path):
    combined_data = []

    for patient_name in os.listdir(root_path):
        patient_folder = os.path.join(root_path, patient_name)
        if os.path.isdir(patient_folder):
            csv_files = [f for f in os.listdir(patient_folder) if f.endswith('.csv')]
            if csv_files:
                csv_path = os.path.join(patient_folder, csv_files[0])
                df = pd.read_csv(csv_path, header=None)
                df.columns = ['Feature', 'Value']
                df['Patient'] = patient_name
                df = df.pivot(index='Patient', columns='Feature', values='Value').reset_index()
                combined_data.append(df)
            else:
                print(f"No CSV file found in {patient_folder}")

    if combined_data:
        final_df = pd.concat(combined_data, ignore_index=True)
        output_path = os.path.join(root_path, 'combined_output.csv')
        final_df.to_csv(output_path, index=False)
        print(f"\nCombined file saved as '{output_path}'")
    else:
        print("\nNo data found to combine.")


if __name__ == "__main__":
    root_input = input("Enter the path to the root folder containing all patient folders: ").strip()
    if os.path.exists(root_input):
        read_csvs_from_folder(root_input)
    else:
        print("The specified path does not exist.")

    print("\n-------------------------------------- Process completed --------------------------------------\n")