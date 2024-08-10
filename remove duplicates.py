import pandas as pd

# Read the CSV file
df = pd.read_csv('file.csv')

# Identify duplicate rows
duplicate_rows = df.duplicated(keep='first')

# Remove duplicate rows
df_no_duplicates = df[~duplicate_rows]

# Save the dataframe with no duplicates to a new CSV file
df_no_duplicates.to_csv('file_no_duplicates.csv', index=False)