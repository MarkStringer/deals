import re
import csv
import sys
from collections import defaultdict
from prettytable import PrettyTable

# Check if filenames are provided as command-line arguments
if len(sys.argv) < 2:
    print("Please provide the names of the CSV files as command-line arguments.")
    sys.exit(1)

# Create a table to display the status counts with the date
table = PrettyTable(['Date', 'Status', 'Count'])

# Loop through each filename provided
for filename in sys.argv[1:]:
    # Extract the date from the filename using regular expressions
    match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
    if match:
        date = match.group()
    else:
        print(f"No valid date found in the filename '{filename}'. Please make sure the date is in the format YYYY-MM-DD.")
        continue

    # Create a defaultdict to store the count of each status
    status_counts = defaultdict(int)

    # Open the CSV file and read its contents
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = row.get('Deal Stage')
                if status and status.startswith('Closed'):
                    status_counts[status] += 1
                else:
                    status_counts['Open'] += 1
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        continue
    except Exception as e:
        print(f"An error occurred while reading the CSV file '{filename}': {str(e)}")
        continue

    # Sort the status counts by keys to maintain the order of statuses
    sorted_status_counts = dict(sorted(status_counts.items()))

    # Add rows to the table with the date and status counts
    for status, count in sorted_status_counts.items():
        table.add_row([date, status, count])

# Print the table
print(table)

