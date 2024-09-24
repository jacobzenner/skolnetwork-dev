import json
import os

# Define the directory containing the JSON files
directory = 'scripts/scraped_data'  # Change this path if necessary

# List of JSON files to process and the columns to remove
json_files = {
    'defense.json': [
        "GS",
        "Yds",
        "TD",
        "Lng",
        "Fmb",
        "Yds",
        "TD",
        "Sfty",
        "Age"
    ],
    'div_passing.json': [
        "1D",
        "Succ%",
        "Lng",
        "Cmp",
        "Att",
        "Age",
        "TD%",
        "Int%",
        "Y/A",
        "AY/A",
        "Y/C",
        "Y/G",
        "Rate",
        "QBR",
        "Sk",
        "GS",
        "Yds.1",
        "Sk%",
        "NY/A",
        "ANY/A",
        "4QC",
        "GWD",
        "Awards"
    ],
    'min_injury_report.json': 'Status',  # Remove entries with "Injured Reserve" status
    'rushing_and_receiving.json': [
        "Age",
        "GS",
        "1D",
        "Succ%",
        "Y/G",
        "Lng",
        "A/G",
        "Tgt",
        "Y/R",
        "R/G",
        "Ctch%",
        "Y/tgt",
        "Touch",
        "Y/Tch",
        "Y/Tgt",
        "YScm",
        "RRTD",
        "Fmb"
    ]
}

# Columns to retain and rename in 'rushing_and_receiving.json'
columns_to_rename = {
    "Rushing', 'Yds": "Rush Yds",
    "Rushing', 'TD": "Rush TD",
    "Receiving', 'Yds": "Rec. Yds",
    "Receiving', 'TD": "Rec. TD"
}

def clean_column_headers(data, rename_map=None):
    cleaned_data = []
    for entry in data:
        cleaned_entry = {}
        for key, value in entry.items():
            # Rename columns if a rename map is provided and the key is in the rename map
            clean_key = rename_map[key] if rename_map and key in rename_map else key
            
            # Clean key to keep only the final part after renaming
            clean_key = clean_key.split(",")[-1].strip("() '")
            
            cleaned_entry[clean_key] = value
        cleaned_data.append(cleaned_entry)
    return cleaned_data




def remove_unwanted_rows(data, file_name):
    """Remove rows based on specific criteria for each file."""
    cleaned_data = []

    for entry in data:
        # Remove rows with 'Team Total' or 'Opp Total' in div_passing or rushing_and_receiving
        if file_name in ['div_passing.json', 'rushing_and_receiving.json', 'defense.json']:
            if 'Player' in entry and (entry['Player'] == 'Team Total' or entry['Player'] == 'Team Totals' or entry['Player'] == 'Opp Total'):
                continue

        # Remove rows with 'Status' as 'Injured Reserve' in min_injury_report
        if file_name == 'min_injury_report.json':
            if entry.get('Status') == 'Injured Reserve':
                continue

        cleaned_data.append(entry)

    return cleaned_data

def remove_unwanted_columns(data, columns_to_remove, retain_columns=None):
    """Remove specific columns from the data."""
    cleaned_data = []
    for entry in data:
        cleaned_entry = {}
        for key, value in entry.items():
            # Retain only specified columns if provided
            if retain_columns and key in retain_columns:
                cleaned_entry[key] = value
            # Otherwise, remove the unwanted columns
            elif key not in columns_to_remove:
                cleaned_entry[key] = value
        cleaned_data.append(cleaned_entry)
    return cleaned_data

def clean_json_file(file_path, file_name, columns_to_remove=None, retain_columns=None, rename_map=None):
    """Clean the JSON file according to specified rules and overwrite the original file."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Clean the column headers and rename specific columns
    cleaned_data = clean_column_headers(data, rename_map)

    # Remove unwanted rows
    cleaned_data = remove_unwanted_rows(cleaned_data, file_name)

    # Remove unwanted columns if specified
    if columns_to_remove:
        cleaned_data = remove_unwanted_columns(cleaned_data, columns_to_remove, retain_columns)

    # Write the cleaned data back to the original file
    with open(file_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)
    print(f"Cleaned data saved to {file_path}")

# Iterate over each JSON file in the directory and clean it
for json_file, columns_to_remove in json_files.items():
    file_path = os.path.join(directory, json_file)
    if os.path.exists(file_path):
        # For 'rushing_and_receiving.json', retain specific columns and rename them
        if json_file == 'rushing_and_receiving.json':
            retain_columns = list(columns_to_rename.values())  # Retain renamed columns
            clean_json_file(file_path, json_file, columns_to_remove, retain_columns, columns_to_rename)
        else:
            clean_json_file(file_path, json_file, columns_to_remove)
    else:
        print(f"File {json_file} not found in {directory}")
