#!/bin/bash

# Calculate the date 90 days ago
start_date=$(date -v-90d +%Y-%m-%d)

# Loop through each day from start_date to today
current_date=$start_date
end_date=$(date +%Y-%m-%d)

while [[ "$current_date" < "$end_date" ]]; do
  for country in Hungary Moldova Poland Romania Slovakia; do
    file_path="data/$current_date/$country.csv"
    
    if [[ -f "$file_path" ]]; then
      echo "File $file_path already exists. Skipping."
    else
      # Run the Python script to load data for the current date
      python3 load.py --date "$current_date"
      
      # Pause for 1 second
      sleep 1
    fi
  done
  
  # Increment the date by one day
  current_date=$(date -j -v+1d -f %Y-%m-%d "$current_date" +%Y-%m-%d)
done

echo "Backfill completed for the last 90 days."
