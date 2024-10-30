import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the property URLs from the JSON file
with open('property_urls.json', 'r') as f:
    property_urls = json.load(f)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def find_trakheesi_urls():
    properties_info = []  # List to store property information
    
    for url in property_urls:
        driver.get(url)
        
        try:
            # Wait for the Trakheesi link to be present
            trakheesi_link_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'styles_desktop_link___qw0V')]"))
            )
            trakheesi_url = trakheesi_link_element.get_attribute('href')

            # Extract bedrooms and bathrooms
            bedrooms = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@data-testid, 'property-attributes-bedrooms')]"))
            ).text.strip()
            
            bathrooms = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@data-testid, 'property-attributes-bathrooms')]"))
            ).text.strip()

            # Append data to properties_info list
            property_data = {
                'Trakheesi URL': trakheesi_url,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms
            }
            properties_info.append(property_data)
            print(f"Found property data: {property_data}")
        
        except Exception as e:
            print(f"Failed to find data for {url}: {e}")

    # Save property information to a JSON file
    with open('properties_info.json', 'w') as f:
        json.dump(properties_info, f, indent=4)

    driver.quit()

# Run the function to find Trakheesi URLs and property info
find_trakheesi_urls()
