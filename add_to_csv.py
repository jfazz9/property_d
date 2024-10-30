import json
import pandas as pd
import os

def update_csv_from_json():
    # Load the final property data from JSON
    with open('json_files/final_property_info.json', 'r') as f:
        final_property_data = json.load(f)

    # Convert the final property data into a DataFrame
    new_data_df = pd.DataFrame(final_property_data)

    # Define the CSV file name
    csv_file = 'data/final_property_info.csv'

    # Check if the CSV file already exists
    if os.path.exists(csv_file):
        # Load the existing CSV data into a DataFrame
        existing_data_df = pd.read_csv(csv_file)

        # Combine the new and existing DataFrames, keeping only unique entries
        combined_data_df = pd.concat([existing_data_df, new_data_df]).drop_duplicates(subset=['Property Value (AED)', 'Property Size (Sqm)'], keep='first')

    else:
        # If the CSV does not exist, use the new data as the combined data
        combined_data_df = new_data_df

    # Save the combined DataFrame back to CSV
    combined_data_df.to_csv(csv_file, index=False)

    print(f"Data saved to '{csv_file}' with {len(combined_data_df)} total entries.")

# Run the function to update the CSV
update_csv_from_json()
