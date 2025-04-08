# Fusión --> Normalización --> Diferencia --> Mejores características

import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from utils.utils import yes_or_no


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
        print(f"\n    [√] Combined file saved as '{output_path}'")
        return output_path
    else:
        print("\n    [X] No data found to combine.")
        return None


def normalize_csv(file_path):
    df = pd.read_csv(file_path)

    ids = df.iloc[:, 0]
    data = df.iloc[:, 1:]

    scaler = MinMaxScaler(feature_range=(-1, 1))
    normalized_data = scaler.fit_transform(data)

    normalized_df = pd.DataFrame(normalized_data, columns=data.columns)
    normalized_df.insert(0, 'Patient', ids)

    output_path = file_path.replace('.csv', '_normalized.csv')
    normalized_df.to_csv(output_path, index=False)

    print(f"\n    [√] Normalized data saved as '{output_path}'")
    return output_path


def compute_pre_post_difference(file_path):
    df = pd.read_csv(file_path)

    df['Patient'] = df['Patient'].astype(str)
    df['BaseID'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    pre_df = df[df['Patient'].str.contains('PRE', case=False)].copy()
    post_df = df[df['Patient'].str.contains('POST', case=False)].copy()

    pre_df['BaseID'] = pre_df['BaseID']
    post_df['BaseID'] = post_df['BaseID']

    merged_df = pd.merge(pre_df, post_df, on='BaseID', suffixes=('_PRE', '_POST'))

    feature_cols = [col for col in merged_df.columns if '_PRE' in col and col != 'Patient_PRE']
    diff_data = {}

    for col in feature_cols:
        base_col = col.replace('_PRE', '')
        diff_data[base_col] = (merged_df[col] - merged_df[base_col + '_POST']).abs()

    result_df = pd.DataFrame(diff_data)
    result_df.insert(0, 'Patient', merged_df['BaseID'])

    output_path = file_path.replace('.csv', '_diff.csv')
    result_df.to_csv(output_path, index=False)

    print(f"\n    [√] Difference PRE vs POST calculated and saved as '{output_path}'")
    return output_path


def get_sorted_features(diff_file_path):
    df = pd.read_csv(diff_file_path)
    df_features = df.drop(columns=['Patient'])

    std_diffs = df_features.std()
    std_diffs = std_diffs[std_diffs > 0].sort_values()

    print("\nAll features ordered by standard deviation (from most stable to most variable):")
    for i, (feature, score) in enumerate(std_diffs.items(), start=1):
        print(f"{i:3d}. {feature:50s} --> Deviation: {score:.10f}")


def main():
    root_input = input("Enter the path to the root folder containing all patient folders: ").strip()
    if os.path.exists(root_input):
        combined_csv = read_csvs_from_folder(root_input)

        if combined_csv:
            do_norm = yes_or_no("\nDo you want to normalize the combined data? (yes/no): ")
            final_csv = normalize_csv(combined_csv) if do_norm == 'yes' else combined_csv

            do_diff = yes_or_no("\nDo you want to compute the difference between PRE and POST tests? (yes/no): ")
            if do_diff == 'yes':
                diff_csv = compute_pre_post_difference(final_csv)

                do_top = yes_or_no("\nDo you want to list all features ordered by stability? (yes/no): ")
                if do_top == 'yes':
                    get_sorted_features(diff_csv)

    else:
        print("    [X] The specified path does not exist.")

    print("\n-------------------------------------- Process completed --------------------------------------\n")


if __name__ == "__main__":
    main()
