from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Set up Chrome options to disable GPU if necessary
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering

# Initialize WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.propertyfinder.ae/en/buy/properties-for-sale.html")

try:
    # Step 1: Wait for the location search form container to be present
    location_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "styles_filters-form__location__KfoYU"))
    )
    print("Location search form container located successfully.")

    # Step 2: Find the input field within this container and ensure it is clickable
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, "input"))
    )
    search_box.send_keys("Arabian Ranches 2")
    print("Search term entered successfully.")

    # Step 3: Wait for the dropdown suggestions to appear
    time.sleep(1)  # Allow a brief moment for suggestions to populate

    # Locate all suggestion buttons
    suggestions = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@data-testid, 'multi-selection-autocomplete-template-suggestion-button')]"))
    )

    # Loop through suggestions to find the correct one
    for suggestion in suggestions:
        if "Arabian Ranches 2" in suggestion.text.strip():
            suggestion.click()  # Click the correct suggestion
            print("Matching suggestion for 'Arabian Ranches 2' selected.")
            break

    # Step 4: Wait for search results to load
    time.sleep(5)  # Adjust this based on your internet speed

    # Step 5: Click the 'Find' button after selecting the suggestion
    find_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="filters-form-btn-find"]'))
    )
    find_button.click()  # Click the 'Find' button
    print("Find button clicked.")

    # Step 6: Wait for the search results page to load
    time.sleep(5)  # Adjust this as needed

    # Step 7: Locate and click the 'Sort' button to open the dropdown
    sort_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="filters-sort"]'))
    )
    sort_button.click()  # Click the sort button to open dropdown
    print("Sort button clicked.")

    # Step 8: Wait for sorting options to appear
    time.sleep(2)  # Allow time for dropdown options to populate

    # Locate the 'Newest' option using the provided class
        # Step 9: Locate the 'Newest' option using its class
    newest_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'styles-module_dropdown-content__item__thioe') and contains(., 'Newest')]"))
    )
    # Click the 'Newest' option
    newest_option.click()  # Click the 'Newest' option
    print("Sorting by 'Newest'.")


    # Step 7: Locate all property cards
    property_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='property-card-module_property-card__link__L6AKb']"))
    )

    # Step 8: Extract information from the first 3 properties
    # Store the URLs in a list
    urls = []
    for i in range(min(3, len(property_links))):  # Limit to first 3 properties
        property_card = property_links[i]
        urls.append(property_card.get_attribute('href'))  # Get the property link

    # Save URLs to a JSON file
    with open('property_urls.json', 'w') as f:
        json.dump(urls, f)
    print(f"Saved property URLs: {urls}")

    # Wait to observe the results
    time.sleep(20)

except Exception as e:
    print(f"An error occurred: {e}")

# Uncomment the following line when ready to close the browser automatically
# driver.quit()
