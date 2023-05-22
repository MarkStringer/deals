import pandas as pd
import matplotlib.pyplot as plt
import argparse
from matplotlib.dates import DateFormatter, WeekdayLocator

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The path to the csv file to be processed.")
args = parser.parse_args()

# read the csv file into a pandas DataFrame
df = pd.read_csv(args.filename)

# sort the DataFrame by the Create Date column and convert it to datetime
df['Create Date'] = pd.to_datetime(df['Create Date'])
df = df.sort_values('Create Date')

# Get all unique stages that start with "Closed"
closed_stages = df['Deal Stage'][df['Deal Stage'].str.startswith('Closed')].unique()

# Loop over all unique closed stages
for stage in closed_stages:
    # create a new column that counts the occurrences of each "Closed" stage
    mask = df['Deal Stage'] == stage
    df[f'{stage}_count'] = mask.astype(int).cumsum()

# create a new column that counts the occurrences of statuses that don't start with "Closed"
not_closed_mask = ~df['Deal Stage'].str.startswith('Closed')
df['not_closed_count'] = not_closed_mask.astype(int).cumsum()

# create a line plot of the final columns against the Create Date column
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.xlabel('Create Date')
plt.ylabel('Counts')

for stage in closed_stages:
    ax.plot(df['Create Date'], df[f'{stage}_count'], label=stage)

ax.plot(df['Create Date'], df['not_closed_count'], label='Not Closed')

plt.legend()
plt.tight_layout()
plt.show()

# output the modified DataFrame to a new csv file
df.to_csv('modified_csv_file.csv', index=False)

