import pandas as pd

# Configuring pandas
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def extract_data(file_path):
    # Read data from Excel file
    df = pd.read_excel(file_path)
    return df


def transform_data(df):
    # Dropping duplicate rows
    df = df.drop_duplicates()

    # Dropping useless columns
    df = df.drop(columns='Not_Useful_Column')

    # Cleaning up the last name column
    df["Last_Name"] = df["Last_Name"].str.strip('.../_')

    # Getting rid of any slashes, dashes, or underscores in the phone numbers
    df['Phone_Number'] = df['Phone_Number'].str.replace(
        '[^a-zA-Z0-9]', '', regex=True)

    # First convert the entire column to strings using a lambda function
    df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))

    # Standardizing the phone numbers
    df["Phone_Number"] = df["Phone_Number"].apply(
        lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

    # Clears out any numbers that have Na or nan
    df["Phone_Number"] = df["Phone_Number"].str.replace('nan--', '')
    df["Phone_Number"] = df["Phone_Number"].str.replace('Na--', '')

    # Here we split the address at every comma and create new columns for Street Address, State, and Zip Code
    df[["Street Address", "State", "Zip Code"]
       ] = df["Address"].str.split(',', expand=True)

    # Standardizing the Paying Customer Column
    df["Paying Customer"] = df["Paying Customer"].str.replace('Yes', 'Y')
    df["Paying Customer"] = df["Paying Customer"].str.replace('No', 'N')

    # Standardizing the Do_Not_Contact Column
    df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('Yes', 'Y')
    df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('No', 'N')

    # Filling any values that are None or NaN
    df = df.replace('N/a', '')
    df = df.fillna('')

    # Dropping rows where Do_Not_Contact is 'Y'
    df = df[df["Do_Not_Contact"] != 'Y']

    # Dropping rows with empty Phone_Number
    df = df[df["Phone_Number"] != '']

    # Reset the index of the dataframe
    df = df.reset_index(drop=True)

    # Drop the Address column since it was split earlier
    df = df.drop("Address", axis=1)

    # Sort the DataFrame by the first name
    df = df.sort_values(by="First_Name")

    df = df.reset_index(drop=True)

    return df


def load_data(df):
    # Loading clean DataFrame
    df.to_excel('./dataset/CLEAN_customer_call_list.xlsx',
                sheet_name='Clean_Sheet', index=False)
    # Printing the cleaned and transformed DataFrame
    print(df)


print('\n**************************')
print('ETL Process Started')
print('**************************\n')

dataframe = extract_data('./dataset/customer_call_list.xlsx')
dataframe = transform_data(dataframe)
load_data(dataframe)
print('\n********************************************************************************************************')
print('ETL Process Complete, open dataset/CLEAN_customer_call_list.xlsx to see the cleaned data....')
print('********************************************************************************************************\n')
