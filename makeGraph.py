import pandas as pd
import matplotlib.pyplot as plt

# read the csv file into a pandas DataFrame
df = pd.read_csv('/home/mark/projects/deals/data/hubspot-crm-exports-all-deals-2023-04-03.csv')

# sort the DataFrame by the Create Date column
df = df.sort_values('Create Date')

# create a new column that counts the occurrences of "Closed" (excluding "Won")
closed_mask = df['Deal Stage'].str.contains('Closed') & ~df['Deal Stage'].str.contains('won')
df['closed_count'] = closed_mask.astype(int).cumsum()

# create a new column that counts the occurrences of statuses that don't contain "Closed" or "Won"
not_closed_mask = ~df['Deal Stage'].str.contains('Closed') & ~df['Deal Stage'].str.contains('won')
df['not_closed_count'] = not_closed_mask.astype(int).cumsum()

# create a new column that counts the occurrences of "Won"
won_mask = df['Deal Stage'].str.contains('won')
df['won_count'] = won_mask.astype(int).cumsum()

# create a line plot of the final three columns against the Create Date column
plt.plot(df['Create Date'], df['closed_count'])
plt.plot(df['Create Date'], df['not_closed_count'])
plt.plot(df['Create Date'], df['won_count'])
plt.xlabel('Create Date')
plt.ylabel('Counts')
plt.legend(['Closed', 'Not Closed', 'Won'])
plt.show()

# output the modified DataFrame to a new csv file
df.to_csv('modified_csv_file.csv', index=False)
