from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Set up headless Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the webpage
driver.get("https://www.pro-football-reference.com/teams/min/2024.htm")

# Wait for tables to load
driver.implicitly_wait(10)

# Specify the table IDs or CSS selectors for the tables you need
table_ids = ["min_injury_report", "div_passing", "rushing_and_receiving", "defense"]

for index, table_id in enumerate(table_ids):
    try:
        # Locate table by ID or CSS selector
        table = driver.find_element(By.ID, table_id)
        html_content = table.get_attribute("outerHTML")
        df = pd.read_html(html_content)[0]
        # Save the DataFrame to a CSV file
        df.to_csv(f"{table_id}.csv", index=False)
        print(f"Saved {table_id}.csv")
    except Exception as e:
        print(f"Failed to find table {table_id}: {e}")

# Close the browser
driver.quit()
