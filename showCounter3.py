import re
import csv
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

# Check if a filename is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the name of the CSV file as a command-line argument.")
    sys.exit(1)

# Get the filename from the command line argument
filename = sys.argv[1]

# Extract the date from the filename using regular expressions
match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
if match:
    date = match.group()
else:
    print("No valid date found in the filename. Please make sure the date is in the format YYYY-MM-DD.")
    sys.exit(1)

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

# Extract the status and count data
statuses = list(status_counts.keys())
counts = list(status_counts.values())

# Create a stacked histogram chart
plt.bar(date, counts, tick_label=statuses)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Status Counts')

# Display the chart
plt.show()
