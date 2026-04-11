#!/bin/bash
# scripts/data_collection.sh
# Handles 2023 Citi Bike dataset with nested monthly zip files.

set -e

mkdir -p data/monthly_trips

# Skip if already have CSV files
if compgen -G "data/monthly_trips/2023-*.csv" > /dev/null; then
    echo "Monthly CSV files already exist. Skipping."
    exit 0
fi

# Download main zip if not present
MAIN_ZIP="data/2023-citibike-tripdata.zip"
if [ ! -f "$MAIN_ZIP" ]; then
    echo "Downloading main dataset zip..."
    wget -O "$MAIN_ZIP" "https://s3.amazonaws.com/tripdata/2023-citibike-tripdata.zip"
else
    echo "Main zip already downloaded."
fi

# Extract main zip to a temp directory
TEMP_DIR="data/temp_nested"
mkdir -p "$TEMP_DIR"
echo "Extracting main zip (contains monthly zips)..."
unzip -q "$MAIN_ZIP" -d "$TEMP_DIR"

# Locate the inner folder (ignore __MACOSX)
INNER_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "2023-citibike-tripdata")
if [ -z "$INNER_DIR" ]; then
    echo "Error: Could not find inner folder 2023-citibike-tripdata"
    exit 1
fi

echo "Found inner folder with monthly zips: $INNER_DIR"

# Process each monthly zip
for month_zip in "$INNER_DIR"/*.zip; do
    # Extract month and year from filename (e.g., 202301-citibike-tripdata.zip)
    base=$(basename "$month_zip")
    if [[ "$base" =~ ^([0-9]{6}) ]]; then
        year_month="${BASH_REMATCH[1]}"
        year="${year_month:0:4}"
        month="${year_month:4:2}"
        csv_name="${year}-${month}.csv"
        
        echo "Processing $base -> $csv_name"
        
        # Extract the CSV from the monthly zip
        # Unzip into a temporary subdirectory to avoid clutter
        temp_month="data/temp_month"
        mkdir -p "$temp_month"
        unzip -q "$month_zip" -d "$temp_month"
        
        # Find the CSV file inside (there should be exactly one)
        csv_file=$(find "$temp_month" -name "*.csv" | head -n 1)
        if [ -n "$csv_file" ]; then
            mv "$csv_file" "data/monthly_trips/$csv_name"
            echo "  Saved $csv_name"
        else
            echo "  Warning: No CSV found in $base"
        fi
        
        # Clean up temp month folder and delete the monthly zip to save space
        rm -rf "$temp_month"
        rm "$month_zip"
    else
        echo "Skipping unrecognized zip: $base"
    fi
done

# Clean up temporary directories
rm -rf "$TEMP_DIR"

echo "Data collection complete. CSV files are in data/monthly_trips/"
echo "Main zip preserved at $MAIN_ZIP"
