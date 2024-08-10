import pandas as pd
import os

def process_csv(input_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Create an empty DataFrame to store the processed data
    new_df = pd.DataFrame(columns=['Name', 'Email', 'Phone'])

    # Iterate over each row in the original DataFrame
    for index, row in df.iterrows():
        if not pd.isna(row['Emails']):
            emails = row['Emails'].split(',')  # Assuming the column name for emails is 'Emails'
        else:
            continue

        if not pd.isna(row['Phone']):
            phones = row['Phone'].split(',')
            if isinstance(phones, list):
                phones_str = ', '.join(phones)
            else:
                phones_str = phones

        # Create entries for each email in the row
        for email in emails:
            # Assign the email under both 'Name' and 'Email' headers
            new_row = {'Name': email, 'Email': email}

            # Assign the phone numbers to the 'Phone' header
            if not pd.isna(row['Phone']):
                new_row['Phone'] = phones_str

            # Append the new row to the new DataFrame
            new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

    # Write the new DataFrame to a new CSV file
    #new_df.to_csv(output_file, index=False)
    mode = 'w' if not os.path.exists(output_file) else 'a'
    new_df.to_csv(output_file, index=False, mode=mode, header=mode == 'w')

if __name__ == '__main__':
    # Specify the input and output file paths
    input_file = 'company_data.csv'
    output_file = 'emails.csv'

    # Call the function to process the CSV
    process_csv(input_file, output_file)