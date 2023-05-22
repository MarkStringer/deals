import re
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Check if filenames are provided as command-line arguments
if len(sys.argv) < 2:
    print("Please provide the names of the CSV files as command-line arguments.")
    sys.exit(1)

# Create a defaultdict to store the count of each status for each date
status_counts = defaultdict(lambda: defaultdict(int))
first_week_counts = defaultdict(int)

# Loop through each filename provided
for filename in sys.argv[1:]:
    # Extract the date from the filename using regular expressions
    match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
    if match:
        date = match.group()
    else:
        print(f"No valid date found in the filename '{filename}'. Please make sure the date is in the format YYYY-MM-DD.")
        continue

    # Open the CSV file and read its contents
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = row.get('Deal Stage')
                if status and status.startswith('Closed'):
                    status_counts[date][status] += 1
                else:
                    status_counts[date]['Open'] += 1
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        continue
    except Exception as e:
        print(f"An error occurred while reading the CSV file '{filename}': {str(e)}")
        continue

# Extract unique statuses and dates
statuses = sorted(set(status for date in status_counts for status in status_counts[date]))
dates = sorted(status_counts.keys())

# Save first week counts
if dates:
    first_week_counts = status_counts[dates[0]]

# Prepare data for change relative to the first week
status_data = {status: [status_counts[date][status] - first_week_counts[status] for date in dates] for status in statuses}

# Generate bar chart
index = np.arange(len(dates))
bar_width = 0.4

fig, ax = plt.subplots()
colors = plt.cm.Set3(np.linspace(0, 1, len(statuses)))

for i, status in enumerate(statuses):
    ax.bar(index + i * bar_width, status_data[status], bar_width, label=status, color=colors[i])

ax.set_xlabel('Date')
ax.set_ylabel('Change in Count')
ax.set_title('Change in Status Counts Relative to the First Week')
ax.set_xticks(index + bar_width * len(statuses) / 2)
ax.set_xticklabels(dates, rotation=45)
ax.legend()

plt.tight_layout()
plt.show()

