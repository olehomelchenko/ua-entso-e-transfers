import pandas as pd
from datetime import datetime
import os
import argparse
import logging
import json

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

country_codes = config["country_codes"]
url_template = config["url_template"]


def load_to_csv(load_date, country):
    try:
        date_dmy = datetime.strptime(load_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError as e:
        logging.error(f"Invalid date format for {load_date}: {e}")
        return

    url = url_template.format(datetime=date_dmy, border_values=country_codes[country])

    try:
        res = pd.read_html(url)[0]
        res.columns = ["_".join(col).strip() for col in res.columns.values]
    except ValueError as e:
        logging.error(f"Failed to parse HTML for {country} on {load_date}: {e}")
        return
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while fetching data for {country} on {load_date}: {e}"
        )
        return

    directory = f"data/{load_date}"
    file_path = os.path.join(directory, f"{country}.csv")
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        res.to_csv(file_path, index=False)
        logging.info(f"Loaded to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save CSV for {country} on {load_date}: {e}")


def main(date):
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        return

    # Validate country
    invalid_countries = [
        country for country in country_codes if country not in country_codes
    ]
    if invalid_countries:
        logging.error(f"Invalid country codes: {', '.join(invalid_countries)}")
        return

    for country, code in country_codes.items():
        load_to_csv(date, country)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some keyword arguments.")
    parser.add_argument(
        "--date", type=str, required=True, help="Date in YYYY-MM-DD format"
    )

    args = parser.parse_args()

    main(date=args.date)
