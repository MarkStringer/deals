import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process a CSV file.')

# Add the arguments
parser.add_argument('CSVfile', metavar='CSVfile', type=str, help='the path to the CSV file')

# Execute the parse_args() method
args = parser.parse_args()

# Load the CSV file
df = pd.read_csv(args.CSVfile)

# Convert 'Last Modified Date' and 'Create Date' to datetime
df['Last Modified Date'] = pd.to_datetime(df['Last Modified Date'])
df['Create Date'] = pd.to_datetime(df['Create Date'])

# Sort by 'Last Modified Date'
df = df.sort_values('Last Modified Date')

# Create columns for each deal stage
df['Closed: abandoned'] = df['Deal Stage'] == 'Closed: abandoned'
df['Closed: lost'] = df['Deal Stage'] == 'Closed: lost'
df['Closed: won'] = df['Deal Stage'] == 'Closed: won'
df['Other Status'] = ~df['Deal Stage'].isin(['Closed: abandoned', 'Closed: lost', 'Closed: won'])

# Group by 'Create Date' and count occurrences
df_grouped = df.groupby(df['Create Date'].dt.date).sum()

# Plot
df_grouped[['Closed: abandoned', 'Closed: lost', 'Closed: won', 'Other Status']].plot(kind='line')
plt.title('Deal Stages over Time')
plt.xlabel('Create Date')
plt.ylabel('Count')
plt.show()

