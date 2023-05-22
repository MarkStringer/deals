import argparse
import pandas as pd
from datetime import datetime, timedelta
import sys

def read_csv_and_filter(filename):
    # Read the csv file into a pandas DataFrame
    df = pd.read_csv(filename)

    # Convert the "Last Modified Date" column to datetime format
    df["Last Modified Date"] = pd.to_datetime(df["Last Modified Date"])

    # Extract date from filename
    date_str = filename.split('/')[-1].split('.')[0]
    try:
        reference_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Could not extract a valid date from the filename. Exiting.")
        sys.exit()

    # Calculate the datetime one week before the reference date
    one_week_before = reference_date - timedelta(weeks=1)

    # Filter rows where "Last Modified Date" is within the week before the reference date
    filtered_df = df[df["Last Modified Date"] >= one_week_before]

    # Output the filtered DataFrame to a csv file
    filtered_df.to_csv('output.csv', index=False)

def main():
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description='Process a csv file.')
    parser.add_argument('filename', type=str, help='Name of the csv file to process')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the function with the filename argument
    read_csv_and_filter(args.filename)

if __name__ == "__main__":
    main()

