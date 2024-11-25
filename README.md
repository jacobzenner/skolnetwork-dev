# Skol Network Website

This repository contains the code for the Skol Network website, accessible at [skolnetwork.com](https://www.skolnetwork.com). The website is hosted in an AWS S3 bucket and distributed globally using AWS CloudFront for faster loading times. GitHub Actions are used to manage web scraping, deployment, and cache invalidation processes.

## Website Overview
The Skol Network website is dedicated to providing statistical data, news, articles, and updates on the Minnesota Vikings and NFC North teams. It features sections such as:
- **Team Schedule**: Displays the current season schedule.
- **Twitter Feed**: Embeds the latest tweets from the official Minnesota Vikings Twitter account.
- **Injury Report**: Provides a summary of the team's injury status.
- **Statistics**: Displays passing, rushing, receiving, and defensive stats.
- **NFC North Overview**: Shows the NFC North division standings.

The frontend is built using HTML and Tailwind CSS, ensuring a responsive and clean user experience.

## Web Scraping Process
Data for the website is automatically updated by scraping content from relevant sports websites using Selenium and Pandas. The scraping scripts are run as part of a scheduled GitHub Action. The scraped data is stored as JSON files, which are then used to dynamically populate the website content.

### Scraping Details
- **Tooling**: The scraping process utilizes Selenium to navigate and extract HTML content, which is then parsed with Pandas to generate JSON files.
- **Sources**: The data is scraped from sources such as [Pro-Football-Reference](https://www.pro-football-reference.com), targeting relevant tables like NFC, AFC, injury reports, and player stats.
- **Scripts**: The scraping logic is contained in scripts like `scrape.py` and `Lscrape.py`, with tables extracted by ID and saved to JSON files. For example:
  - `NFC` and `AFC` divisions are saved as `NFC.json` and `AFC.json` respectively.
  - Player stats and injury reports are extracted from team pages.

## Cleaning JSON Data
The scraped JSON files are further processed and cleaned to ensure data quality and consistency:
- **Cleaning Rules**: Unwanted columns are removed, rows with irrelevant data (e.g., team totals) are filtered out, and columns are renamed to a more readable format.
- **Scripts**: The cleaning process is handled by `clean.py` and `Lclean.py`, which apply transformations like removing injured reserve players from the injury report or aggregating division data.

## Deployment Workflow
The deployment of the Skol Network website is automated using GitHub Actions:
1. **Web Scraping and Cleaning**: The scraping and data cleaning scripts are executed on a scheduled basis to keep the site content updated.
2. **Deployment**: The updated content is then deployed to the AWS S3 bucket hosting the website.
3. **CloudFront Invalidation**: After deployment, a CloudFront invalidation is triggered to ensure users get the latest content without caching issues.

## Requirements
To run the scraping scripts locally or modify the setup, you'll need the following dependencies (specified in `requirements.txt`):
- `requests`
- `beautifulsoup4`
- `selenium`
- `pandas`
- `lxml`
- `json`

Make sure to install these dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Scraping Script
To run the scraping script manually:
1. Download the appropriate ChromeDriver for Selenium.
2. Set up a Python environment with the dependencies installed.
3. Run the script using:
```sh
python scrape.py
```

The script will generate JSON files in the `scripts/scraped_data` directory, which are then used by the frontend.

