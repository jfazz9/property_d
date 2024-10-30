import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the Trakheesi URLs from the JSON file
with open('properties_info.json', 'r') as f:
    properties_info = json.load(f)

trakheesi_urls = [property['Trakheesi URL'] for property in properties_info]

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def extract_property_info():
    all_property_info = []  # List to store all property details

    for link in trakheesi_urls:
        driver.get(link)

        # Wait for the property information to load
        try:
            # Locate the property details container
            property_details_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mt-4.border-0.card"))
            )

            # Locate the relevant property details
            property_details = property_details_container.find_elements(By.CSS_SELECTOR, "div.flex-grid.flex-grid-col-2")

            property_data = {}
            print(f"Extracting information from {link}...")  # Debugging line

            # Extract relevant property information
            for grid in property_details:
                rows = grid.find_elements(By.TAG_NAME, 'div')
                for row in rows:  # Process each row for labels and values
                    text = row.text.strip().split("\n")  # Split on new line
                    if len(text) == 2:  # Ensure it's a key-value pair
                        label = text[0].strip()  # The label
                        value = text[1].strip()  # The value
                        property_data[label] = value

            # Debugging output
            print(f"Data collected for {link}: {property_data}")  # Debugging line

            # Create a dictionary to hold the extracted information
            property_info = {}
            if "Property Value(AED)" in property_data:
                property_info['Property Value (AED)'] = property_data['Property Value(AED)']
                print(f"Property Value: {property_info['Property Value (AED)']} AED")
            if "Property Size(Sqm)" in property_data:
                property_info['Property Size (Sqm)'] = property_data['Property Size(Sqm)']
                print(f"Property Size (Sqm): {property_info['Property Size (Sqm)']} sqm")

            # Append the property information to the list only if it's not empty
            if property_info:  # Check if there's any information collected
                all_property_info.append(property_info)
            else:
                print(f"No relevant information found for {link}.")

        except Exception as e:
            print(f"An error occurred while accessing {link}: {e}")

    # Output the collected property information
    print("Collected Property Information:")
    for info in all_property_info:
        print(info)

    with open('tracksi_info.json', 'w') as f:
        json.dump(all_property_info, f, indent=4)






# Run the function to extract property information
extract_property_info()
driver.quit()