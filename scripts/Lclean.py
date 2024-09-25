import json
import os

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to clean JSON files based on rules defined in the arguments
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

# Function to clean column headers based on a rename map
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

# Function to remove unwanted rows from the JSON data
def remove_unwanted_rows(data, file_name):
    cleaned_data = []
    for entry in data:
        # Remove rows with 'Team Total' or 'Opp Total'
        if file_name in ['div_passing.json', 'rushing_and_receiving.json', 'defense.json']:
            if 'Player' in entry and entry['Player'] in ['Team Total', 'Team Totals', 'Opp Total']:
                continue

        # Remove rows with 'Status' as 'Injured Reserve'
        if file_name == 'min_injury_report.json':
            if entry.get('Status') == 'Injured Reserve':
                continue

        cleaned_data.append(entry)
    return cleaned_data

# Function to remove unwanted columns from the JSON data
def remove_unwanted_columns(data, columns_to_remove, retain_columns=None):
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

# Function to create divisions.json from AFC and NFC data
def create_divisions_json(afc_data, nfc_data, output_file):
    divisions = {}

    # Helper function to process each conference data
    def process_conference(data):
        current_division = None
        for record in data:
            # Check if it's a division row
            if record["Tm"] in ["AFC East", "AFC North", "AFC South", "AFC West", "NFC East", "NFC North", "NFC South", "NFC West"]:
                current_division = record["Tm"]
                # Initialize the division in the dictionary
                divisions[current_division] = []
            else:
                # Add the team to the current division
                if current_division:
                    divisions[current_division].append({
                        "team": record["Tm"],
                        "W": record["W"],
                        "L": record["L"],
                        "PD": record["PD"]  # Only include Wins, Losses, and Point Differential
                    })

    # Process AFC and NFC data
    process_conference(afc_data)
    process_conference(nfc_data)

    # Create a new structured JSON with only the divisions and associated teams
    formatted_data = []
    for division, teams in divisions.items():
        formatted_data.append({
            "division": division,
            "teams": teams
        })

    # Save the new structured JSON to a file in the scraped_data directory
    with open(output_file, 'w') as f:
        json.dump(formatted_data, f, indent=4)
    print(f"Formatted data saved to {output_file}")

# Define file paths and rules for cleaning
directory = 'scraped_data'
json_files = {
    'defense.json': ["GS", "Yds", "TD", "Lng", "Fmb", "Yds", "TD", "Sfty", "Age"],
    'div_passing.json': ["1D", "Succ%", "Lng", "Cmp", "Att", "Age", "TD%", "Int%", "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "QBR", "Sk", "GS", "Yds.1", "Sk%", "NY/A", "ANY/A", "4QC", "GWD", "Awards"],
    'min_injury_report.json': 'Status',  # Remove entries with "Injured Reserve" status
    'rushing_and_receiving.json': ["Age", "GS", "1D", "Succ%", "Y/G", "Lng", "A/G", "Tgt", "Y/R", "R/G", "Ctch%", "Y/tgt", "Touch", "Y/Tch", "Y/Tgt", "YScm", "RRTD", "Fmb"]
}

# Columns to retain and rename in 'rushing_and_receiving.json'
columns_to_rename = {
    "Rushing', 'Yds": "Rush Yds",
    "Rushing', 'TD": "Rush TD",
    "Receiving', 'Yds": "Rec. Yds",
    "Receiving', 'TD": "Rec. TD"
}

# Clean each JSON file according to the defined rules
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

# Load the JSON data from AFC and NFC files
afc_file = os.path.join(directory, "AFC.json")
nfc_file = os.path.join(directory, "NFC.json")
if os.path.exists(afc_file) and os.path.exists(nfc_file):
    afc_data = load_json(afc_file)
    nfc_data = load_json(nfc_file)

    # Create divisions.json file
    create_divisions_json(afc_data, nfc_data, os.path.join(directory, "divisions.json"))
else:
    print("AFC or NFC JSON files not found in the directory.")
