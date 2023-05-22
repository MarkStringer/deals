import csv
import sys
from collections import defaultdict
from prettytable import PrettyTable

# Check if filenames are provided as command-line arguments
if len(sys.argv) < 2:
    print("Please provide the names of the CSV files as command-line arguments.")
    sys.exit(1)

# Loop through each filename provided
for filename in sys.argv[1:]:
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

    # Create a table to display the status counts
    table = PrettyTable(['Status', 'Count'])
    for status, count in status_counts.items():
        table.add_row([status, count])

    # Print the table
    print(f"Status counts for file '{filename}':")
    print(table)
    print()  # Add an empty line between files

