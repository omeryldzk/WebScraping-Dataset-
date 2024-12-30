import pandas as pd
from fuzzywuzzy import fuzz, process
import warnings

# Load data
yok_df = pd.read_csv("updated_data.csv")
fee_df = pd.read_csv("fee_updated.csv")

# Convert the 'Ücret' column to numeric, handling non-numeric values
fee_df['Ücret'] = pd.to_numeric(fee_df['Ücret'], errors='coerce')
yok_df['scholarshipRate'] = pd.to_numeric(yok_df['scholarshipRate'], errors='coerce')
fee_df = fee_df.dropna(subset=['Ücret'])  # Remove rows with NaN in 'Ücret'

# Define inflation rates
inflation_rates = {
    2019: 1.1,
    2020: 1.3,
    2021: 1.8,
    2022: 2.1,
    2023: 2,
    2024: 1.9,
    2025: 2,
}

# Normalize strings by removing spaces and converting to lowercase
def normalize_string(value):
    if isinstance(value, str):
        return value.replace(" ", "").lower()
    return value

# Apply normalization to relevant columns in both dataframes
yok_df['departmentName'] = yok_df['departmentName'].apply(normalize_string)
yok_df['faculty'] = yok_df['faculty'].apply(normalize_string)
fee_df['Bölüm/Fakülte'] = fee_df['Bölüm/Fakülte'].apply(normalize_string)

# Adjust fee based on inflation
def adjust_fee(base_fee, base_year, target_year):
    base_fee = float(base_fee)
    adjustment_factor = 1.0
    if base_year < target_year:
        for year in range(base_year, target_year):
            adjustment_factor *= inflation_rates[year]
    elif base_year > target_year:
        for year in range(target_year, base_year):
            adjustment_factor /= inflation_rates[year]
    return base_fee * adjustment_factor

# Update fuzzy_match function to use normalized strings
def fuzzy_match(value, choices, threshold=70):
    result = process.extractOne(value, choices, scorer=fuzz.token_set_ratio)
    if result:
        match, score = result
        return match if score >= threshold else None
    return None

# Adjust fee based on scholarship difference
def adjust_for_scholarship(base_fee, base_scholarship, target_scholarship):
    base_fee = float(base_fee)
    if base_scholarship != target_scholarship:
        adjustment_factor = (100 - target_scholarship) / (100 - base_scholarship)
        return base_fee * adjustment_factor
    return base_fee

# Calculate the average fee for a given year, considering scholarships
def calculate_yearly_average_fee(year):
    # Filter data for the given year and calculate the average fee after adjusting for scholarship
    yearly_data = fee_df[fee_df['Akademik yıl'] == year]
    if not yearly_data.empty:
        adjusted_fees = yearly_data.apply(
            lambda row: adjust_for_scholarship(row['Ücret'], row['burs_oranı'], 0), axis=1
        )
        return adjusted_fees.mean()
    return None

# Main function to find the best fee
def find_best_fee(yok_row):
    uni = normalize_string(yok_row['universityName'])
    dept = normalize_string(yok_row['departmentName'])
    faculty = normalize_string(yok_row['faculty'])
    scholarship = yok_row['scholarshipRate']
    year = yok_row['academicYear']

    if yok_row['universityType'].lower() == "devlet":
        return 0
    # If the scholarship is 100%, set fee to 0
    if scholarship == 100:
        return 0
    # Find closest university name in fee.csv
    uni_match = fuzzy_match(uni, fee_df['universityName'].unique())

    # Attempt matches with both department and faculty names
    dept_or_faculty_matches = [dept, faculty]

    name_match = None
    for name_option in dept_or_faculty_matches:
        name_match = fuzzy_match(
            name_option, 
            fee_df[fee_df['universityName'] == uni_match]['Bölüm/Fakülte'].unique()
        )
        if name_match:
            break

    # Step 1: Exact match on department/faculty and year, ignoring scholarship initially
    exact_match = fee_df[
        (fee_df['universityName'] == uni_match) &
        (fee_df['Bölüm/Fakülte'] == name_match) &
        (fee_df['Akademik yıl'] == year)
    ]
    if not exact_match.empty:
        found_fee = exact_match['Ücret'].iloc[0]
        found_scholarship = exact_match['burs_oranı'].iloc[0]
        return adjust_for_scholarship(found_fee, found_scholarship, scholarship)

    # Step 2: Check other departments/faculties within the same year
    other_dept_same_year = fee_df[
        (fee_df['universityName'] == uni_match) &
        (fee_df['Akademik yıl'] == year)
    ]
    if not other_dept_same_year.empty:
        found_fee = other_dept_same_year['Ücret'].median()
        found_scholarship = other_dept_same_year['burs_oranı'].median()
        return adjust_for_scholarship(found_fee, found_scholarship, scholarship)

    # Step 3: Check the same department/faculty in other years
    same_dept_other_years = fee_df[
        (fee_df['universityName'] == uni_match) &
        (fee_df['Bölüm/Fakülte'] == name_match)
    ]
    if not same_dept_other_years.empty:
        closest_year = same_dept_other_years['Akademik yıl'].iloc[0]
        closest_fee = same_dept_other_years['Ücret'].iloc[0]
        closest_scholarship = same_dept_other_years['burs_oranı'].iloc[0]
        adjusted_fee = adjust_fee(closest_fee, closest_year, year)
        return adjust_for_scholarship(adjusted_fee, closest_scholarship, scholarship)

    # Step 4: Fallback to similar department/faculty at other universities if no match found
    similar_dept = fuzzy_match(dept, fee_df['Bölüm/Fakülte'].unique())
    if similar_dept:
        dept_match_same_year = fee_df[
            (fee_df['Bölüm/Fakülte'] == similar_dept) &
            (fee_df['Akademik yıl'] == year)
        ]
        if not dept_match_same_year.empty:
            found_fee = dept_match_same_year['Ücret'].median()
            found_scholarship = dept_match_same_year['burs_oranı'].median()
            return adjust_for_scholarship(found_fee, found_scholarship, scholarship)

    # Step 5: Search other departments/faculties in other years
    other_dept_other_years = fee_df[
        (fee_df['universityName'] == uni_match)
    ]
    if not other_dept_other_years.empty:
        closest_year = other_dept_other_years['Akademik yıl'].iloc[0]
        closest_fee = other_dept_other_years['Ücret'].iloc[0]
        closest_scholarship = other_dept_other_years['burs_oranı'].iloc[0]
        adjusted_fee = adjust_fee(closest_fee, closest_year, year)
        return adjust_for_scholarship(adjusted_fee, closest_scholarship, scholarship)

    # If all else fails, use the average fee for the year
    year_avg_fee = calculate_yearly_average_fee(year)
    return year_avg_fee

# Apply function to each row in yök.csv
yok_df['Estimated Fee'] = yok_df.apply(find_best_fee, axis=1)
# Save the updated yök data with estimated fees
yok_df.to_csv("fee_yök.csv", index=False)
