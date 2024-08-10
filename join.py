import pandas as pd

common_column = ''

# Read the first CSV file
df1 = pd.read_csv('file1.csv')

# Read the second CSV file
df2 = pd.read_csv('file2.csv')

# Perform the join operation based on a common column
merged_df = pd.merge(df1, df2, on=common_column, how='inner')

# Save the merged data to a new CSV file
merged_df.to_csv('merged_file.csv', index=False)