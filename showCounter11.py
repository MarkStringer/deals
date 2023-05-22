import re
import csv
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

# Check if filenames are provided as command-line arguments
if len(sys.argv) < 2:
    print("Please provide the names of the CSV files as command-line arguments.")
    sys.exit(1)

# Create a defaultdict to store the count of each status for each date
status_counts = defaultdict(lambda: defaultdict(int))
previous_week_counts = defaultdict(int)

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

# Prepare data for change relative to the previous week
status_data = {}
for status in statuses:
    status_data[status] = []
    for i in range(len(dates)):
        if i == 0:
            status_data[status].append(0)
        else:
            status_data[status].append(status_counts[dates[i]][status] - status_counts[dates[i-1]][status])

# Generate line chart
fig, ax = plt.subplots()
colors = plt.cm.Set3(np.linspace(0, 1, len(statuses)))

for i, status in enumerate(statuses):
    ax.plot(dates, status_data[status], label=status, color=colors[i], marker='o')

ax.set_xlabel('Date')
ax.set_ylabel('Change in Count')
ax.set_title('Weekly Change in Status Counts')
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

