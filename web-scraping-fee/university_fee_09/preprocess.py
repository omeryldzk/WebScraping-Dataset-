import json
import re
import pandas as pd

# Load the JSON data from the file
with open('fixed_result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a list to store the processed data
processed_data = []

# Function to calculate the average fee from a string
def calculate_average_fee(fee_str):
    if isinstance(fee_str, str):
        # Extract all numbers from the string
        numbers = re.findall(r'\d+\.?\d*', fee_str)
        # Convert to float and calculate the average
        if numbers:
            numbers = [float(num.replace('.', '').replace(',', '.')) for num in numbers]
            return sum(numbers) / len(numbers)
    return None

# Process the data
for university, details in data['Universities'].items():
    fees = details['Fees']
    if isinstance(fees, dict):
        for faculty, fee_str in fees.items():
            average_fee = calculate_average_fee(fee_str)
            if average_fee is not None:
                processed_data.append([university, faculty, average_fee, 0, 2019])
    else:
        average_fee = calculate_average_fee(fees)
        if average_fee is not None:
            processed_data.append([university, "Mühendislik", average_fee, 0, 2019])

# Convert the processed data to a DataFrame
df = pd.DataFrame(processed_data, columns=['universityName', 'Bölüm/Fakülte', 'Ücret', 'burs_oranı', 'Akademik yıl'])
# Fill Academic year with 2019 if it's missing
df['Akademik yıl'] = df['Akademik yıl'].fillna(2019)

# Save the DataFrame to a CSV file
df.to_csv('processed_fees.csv', index=False, encoding='utf-8')

print("Processed data saved to 'processed_fees.csv'")