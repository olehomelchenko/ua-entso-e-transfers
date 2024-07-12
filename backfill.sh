#!/bin/bash

# Function to print usage
print_usage() {
  echo "Usage: $0 -s START_DATE -e END_DATE"
  echo "Example: $0 -s 2024-04-01 -e 2024-07-01"
}

# Parse command-line arguments
while getopts 's:e:' flag; do
  case "${flag}" in
    s) start_date="${OPTARG}" ;;
    e) end_date="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

# Check if start_date and end_date are set
if [ -z "${start_date}" ] || [ -z "${end_date}" ]; then
  print_usage
  exit 1
fi

# Convert dates to seconds since epoch for comparison
start_date_seconds=$(date -j -f "%Y-%m-%d" "${start_date}" "+%s")
end_date_seconds=$(date -j -f "%Y-%m-%d" "${end_date}" "+%s")

# Check if start_date is before or equal to end_date
if [ "${start_date_seconds}" -gt "${end_date_seconds}" ]; then
  echo "Error: START_DATE should be before or equal to END_DATE"
  exit 1
fi

# Loop through each day from start_date to end_date (inclusive)
current_date="${start_date}"
while [ "$(date -j -f "%Y-%m-%d" "${current_date}" "+%s")" -le "${end_date_seconds}" ]; do
  for country in Hungary Moldova Poland Romania Slovakia; do
    file_path="data/${current_date}/${country}.csv"
    
    if [ -f "${file_path}" ]; then
      echo "File ${file_path} already exists. Skipping."
    else
      # Run the Python script to load data for the current date
      python3 load.py --date "${current_date}"
      
      # Pause for 1 second
      sleep 1
    fi
  done
  # Increment the date by one day
  current_date=$(date -j -v+1d -f "%Y-%m-%d" "${current_date}" "+%Y-%m-%d")
done

echo "Backfill completed from ${start_date} to ${end_date}."
