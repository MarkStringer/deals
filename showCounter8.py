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

# Sort the status_counts dictionary by dates
sorted_status_counts = dict(sorted(status_counts.items()))

# Extract unique statuses and sorted dates
statuses = sorted(set(status for date in sorted_status_counts for status in sorted_status_counts[date]))
dates = list(sorted_status_counts.keys())

# Prepare data for clustered histogram
status_data = {status: [] for status in statuses}
previous_counts = defaultdict(int)

# Calculate deltas from the previous week
for date in dates:
    for status in statuses:
        count = sorted_status_counts[date][status]
        delta = count - previous_counts[status]
        status_data[status].append(delta)
        previous_counts[status] = count

# Generate clustered histogram
bar_width = 0.8 / len(statuses)
index = np.arange(len(dates) - 1)

fig, ax = plt.subplots()
colors = plt.cm.Set3(np.linspace(0, 1, len(statuses)))

for i, status in enumerate(statuses):
    deltas = status_data[status][1:]  # Exclude the first week's delta
    positive_deltas = [delta for delta in deltas if delta > 0]
    negative_deltas = [delta for delta in deltas if delta < 0]
    
    ax.bar(index, positive_deltas, bar_width, label=f"{status} (+)", color=colors[i])
    ax.bar(index, negative_deltas, bar_width, label=f"{status} (-)", color=colors[i], alpha=0.5)

ax.set_xlabel('Date')
ax.set_ylabel('Delta')
ax.set_title('Clustered Histogram of Positive and Negative Deltas from Previous Week')
ax.set_xticks(index)
ax.set_xticklabels(dates[1:], rotation=45)
ax.legend()

plt.tight_layout()
plt.show()

