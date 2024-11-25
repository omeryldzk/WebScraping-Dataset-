import pandas as pd

# Load the dataset
df = pd.read_csv('fee.csv')

# Convert the 'Ücret' column to numeric, forcing errors to NaN
df['Ücret'] = pd.to_numeric(df['Ücret'], errors='coerce')

# Function to set the correct burs_oranı
def set_correct_burs_oranı(group):
    if len(group) > 1:
        min_fee_index = group['Ücret'].idxmin()
        group.loc[group.index != min_fee_index, 'burs_oranı'] = 0
    return group

# Function to set the correct burs_oranı
def set_correct_ücret_oranı(group):
    if len(group) > 1:
        max_fee_index = group['Ücret'].idxmax()
        return group.loc[[max_fee_index]]
    return group

# Apply the function to each group
df = df.groupby(['Üniversite', 'Bölüm/Fakülte', 'Akademik yıl']).apply(set_correct_burs_oranı).reset_index(drop=True)
df = df.groupby(['Üniversite', 'Bölüm/Fakülte', 'burs_oranı','Akademik yıl']).apply(set_correct_ücret_oranı).reset_index(drop=True)

# Remove duplicate rows where all fields are the same
df = df.drop_duplicates()

# Save the updated DataFrame to a new CSV
df.to_csv('fee_updated.csv', index=False)