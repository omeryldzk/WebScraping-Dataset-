import json

# Load the JSON data from the file
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Save the fixed JSON data back to a file
with open('fixed_result.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Fixed JSON data saved to 'fixed_result.json'")