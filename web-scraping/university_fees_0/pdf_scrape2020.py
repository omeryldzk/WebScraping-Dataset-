import pandas as pd

file_path = 'ücret_list.csv'  
df = pd.read_csv(file_path)

df.columns = ['Üniversite', 'Bölüm/Fakülte', 'Ücret']

df['Üniversite'].ffill(inplace=True)

df['Akademik yıl'] = 2020

output_path = '2020_ücret.csv' 
df.to_csv(output_path, index=False)

print("Missing university names filled, 'Year' column added, and saved to:", output_path)
