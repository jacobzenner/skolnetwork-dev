from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json

# Set up WebDriver (make sure to download the appropriate driver for your browser)
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://www.pro-football-reference.com/teams/min/2024.htm")

# Wait for tables to load
driver.implicitly_wait(10)

# Specify the table IDs or CSS selectors for the tables you need
# Replace 'table_id_1', 'table_id_2', etc., with actual table IDs or class names
table_ids = ["min_injury_report", "div_passing", "rushing_and_receiving", "defense"]

for index, table_id in enumerate(table_ids):
    try:
        # Locate table by ID or CSS selector
        table = driver.find_element(By.ID, table_id)
        html_content = table.get_attribute("outerHTML")
        df = pd.read_html(html_content)[0]
        
        # Save the DataFrame to a JSON file
        df.to_json(f"scraped_data/{table_id}.json", orient='records', indent=4)
        print(f"Saved {table_id}.json")
    except Exception as e:
        print(f"Failed to find table {table_id}: {e}")

# Close the browser
driver.quit()

