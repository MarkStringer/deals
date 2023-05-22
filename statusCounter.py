import pandas as pd
import datetime
import matplotlib.pyplot as plt
import sys

# Read the csv file name from command line arguments
if len(sys.argv) != 2:
    print("Please provide the CSV file as an argument.")
    sys.exit()

file_name = sys.argv[1]

# Read the csv file
df = pd.read_csv(file_name)

# Convert "Last modified date" column to datetime
df['Last Modified Date'] = pd.to_datetime(df['Last Modified Date'])

# Get the date one week ago from today
one_week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)

# Filter rows with "Last modified date" in the last week
df_last_week = df[df['Last Modified Date'] >= one_week_ago]

# Count the statuses
status_counts = df_last_week['Deal Stage'].value_counts()

# Plot as a stacked histogram
##status_counts.plot(kind='bar', stacked=True)


# Print the status counts
print(status_counts)


# Show the plot
##plt.xlabel('Status')
#plt.ylabel('Count')
##plt.title('Status Count in the Last Week')
##plt.show()

