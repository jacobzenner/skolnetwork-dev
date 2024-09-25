from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os

# Function to scrape a given URL and table IDs, then save the tables to JSON files
def scrape_tables(url, table_ids, output_dir="scraped_data"):
    # Set up WebDriver (make sure to download the appropriate driver for your browser)
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get(url)

    # Wait for tables to load
    driver.implicitly_wait(10)

    # Ensure the directory exists for saving JSON files
    os.makedirs(output_dir, exist_ok=True)

    for table_id in table_ids:
        try:
            # Locate table by ID or CSS selector
            table = driver.find_element(By.ID, table_id)
            html_content = table.get_attribute("outerHTML")
            df = pd.read_html(html_content)[0]

            # Save the DataFrame to a JSON file
            df.to_json(f"{output_dir}/{table_id}.json", orient='records', indent=4)
            print(f"Saved {table_id}.json in {output_dir}")
        except Exception as e:
            print(f"Failed to find table {table_id}: {e}")

    # Close the browser
    driver.quit()

# Scrape data from the first website (division data)
scrape_tables(
    url="https://www.pro-football-reference.com/years/2024/",
    table_ids=["NFC", "AFC"]
)

# Scrape data from the second website (specific team data)
scrape_tables(
    url="https://www.pro-football-reference.com/teams/min/2024.htm",
    table_ids=["min_injury_report", "div_passing", "rushing_and_receiving", "defense"]
)
