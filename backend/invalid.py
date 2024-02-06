import pandas as pd

# Function to find invalid values in Excel file
def find_invalid_values(excel_file, invalid_values):
    # Load Excel file into pandas dataframe
    df = pd.read_excel(excel_file)
    # Trim the postcode column of any leading or trailing whitespace
    df.iloc[:, 1] = df.iloc[:, 1].str.replace(' ', '')
    
    invalid_rows = []
    
    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        # Check each value in the row for validity
        for col, value in row.items():
            if value in invalid_values:
                invalid_rows.append((index + 2, row.tolist()))  # Adding 2 to index to account for 0-based indexing and header row
                break
    
    return invalid_rows

# Example usage
if __name__ == "__main__":
    # Provide the path to your Excel file
    excel_file = "data/Sample Data - 2019 - UK & Home Students.xlsx"
    
    # List of invalid values to search for
    invalid_values =  ['AZ1078', 'BE3319', 'ED548JP', 'F92HK7F', 'H91VSKW', 'L1533', 'L-4150', 'L-6462', 'LT-93260', 'LV2016', 'R7A0R9', 'T9W1T5', 'V2T4W4']
    
    # Find invalid values in Excel file
    invalid_rows = find_invalid_values(excel_file, invalid_values)
    
    # Print out the row number and contents of each invalid row
    for row_number, row_contents in invalid_rows:
        print(f"Invalid postcode in row {row_number}: {row_contents}")
