import sys
import pandas as pd
import matplotlib.pyplot as plt

# Get the CSV file name from the command line arguments
csv_file_name = sys.argv[1]

# Load your CSV file
df = pd.read_csv(csv_file_name)

# Convert 'Creation Date' to datetime
df['Create Date'] = pd.to_datetime(df['Create Date'])

# Extract year and month from 'Creation Date'
df['YearMonth'] = df['Create Date'].dt.to_period('M')

# Group by 'YearMonth' and count 'Deal Name' (or 'Deal ID')
df_grouped = df.groupby('YearMonth')['Deal Name'].count()

# Create a bar plot
df_grouped.plot(kind='bar')
plt.title('New Deals per Month')
plt.xlabel('Month')
plt.ylabel('Number of Deals')
plt.show()

