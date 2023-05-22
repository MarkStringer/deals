import argparse
import pandas as pd
from datetime import datetime, timedelta

def read_csv_and_filter(filename):
    # Read the csv file into a pandas DataFrame
    df = pd.read_csv(filename)

    # Convert the "Last Modified Date" column to datetime format
    df["Last Modified Date"] = pd.to_datetime(df["Last Modified Date"])

    # Calculate the datetime one week ago
    one_week_ago = datetime.now() - timedelta(weeks=1)

    # Filter rows where "Last Modified Date" is within the last week
    filtered_df = df[df["Last Modified Date"] >= one_week_ago]

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

