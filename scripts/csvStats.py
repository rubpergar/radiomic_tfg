import pandas as pd
import pingouin as pg
from scipy.stats import wilcoxon
import os
import warnings

# Do not show warning errors caused by mathematical issues during calculations
warnings.filterwarnings("ignore", category=RuntimeWarning)


def calculate_icc(original_file):
    df = pd.read_csv(original_file)
    df['Patient'] = df['Patient'].astype(str)
    df['BaseID'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    pre_df = df[df['Patient'].str.contains('PRE', case=False)].copy()
    post_df = df[df['Patient'].str.contains('POST', case=False)].copy()

    icc_dict = {}

    features = [col for col in df.columns if col not in ['Patient', 'BaseID']]
    for feature in features:
        df_icc = pd.DataFrame({
            'targets': pre_df['BaseID'],
            'raters': ['PRE'] * len(pre_df),
            'ratings': pre_df[feature]
        })
        df_post = pd.DataFrame({
            'targets': post_df['BaseID'],
            'raters': ['POST'] * len(post_df),
            'ratings': post_df[feature]
        })

        df_combined = pd.concat([df_icc, df_post], ignore_index=True)
        try:
            icc_val = pg.intraclass_corr(data=df_combined, targets='targets', raters='raters', ratings='ratings')
            icc_value = icc_val[icc_val['Type'] == 'ICC2']['ICC'].values[0]
            icc_dict[feature] = icc_value
        except:
            continue

    return pd.DataFrame.from_dict(icc_dict, orient='index', columns=['icc'])


def calculate_wilcoxon(original_file):
    df = pd.read_csv(original_file)
    df['Patient'] = df['Patient'].astype(str)
    df['BaseID'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    pre_df = df[df['Patient'].str.contains('PRE', case=False)].copy()
    post_df = df[df['Patient'].str.contains('POST', case=False)].copy()

    wlcx_dict = {}
    features = [col for col in df.columns if col not in ['Patient', 'BaseID']]
    for feature in features:
        try:
            stat, p = wilcoxon(pre_df[feature], post_df[feature])
            wlcx_dict[feature] = p
        except:
            continue

    return pd.DataFrame.from_dict(wlcx_dict, orient='index', columns=['pval'])


def filter_features(icc_df, pval_df, icc_thresh=0.8, pval_thresh=0.05):
    merged = icc_df.join(pval_df)
    filtered = merged[
        (merged['icc'] > icc_thresh) &
        (merged['pval'] > pval_thresh)
    ]
    return filtered


if __name__ == "__main__":
    input_path = input("Enter the path to the normalized PRE/POST .csv file: ").strip()

    if os.path.exists(input_path):
        print("\n    [~] Calculating feature statistics...")

        icc_df = calculate_icc(input_path)
        pval_df = calculate_wilcoxon(input_path)

        result = filter_features(icc_df, pval_df)

        print(f"\n    [√] {len(result)} robust features found (ICC > 0.8 and p > 0.05):")
        print(result)

        output_file = os.path.join(os.path.dirname(input_path), 'robust_features.csv')
        result.to_csv(output_file)
        print(f"\n    [✓] Result saved to '{output_file}'")

    else:
        print("\n    [X] File not found. Check the path and try again.")

    print("\n-------------------------------------- Process completed --------------------------------------\n")