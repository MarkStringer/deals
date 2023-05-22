import csv
import sys
from collections import defaultdict
from prettytable import PrettyTable

# Check if a filename is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the name of the CSV file as a command-line argument.")
    sys.exit(1)

# Get the filename from the command line argument
filename = sys.argv[1]

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
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the CSV file: {str(e)}")
    sys.exit(1)

# Create a table to display the status counts
table = PrettyTable(['Status', 'Count'])
for status, count in status_counts.items():
    table.add_row([status, count])

# Print the table
print(table)
