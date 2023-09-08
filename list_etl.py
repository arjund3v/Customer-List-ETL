import pandas as pd

# Configuring pandas
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_excel('./dataset/customer_call_list.xlsx')

# Dropping duplicate rows
df = df.drop_duplicates()

# Dropping useless columns
df = df.drop(columns='Not_Useful_Column')

# Cleaning up the last name column
df["Last_Name"] = df["Last_Name"].str.strip('.../_')


# Getting rid of any slashes, or dashes, or underscored in the phone numbers
df['Phone_Number'] = df['Phone_Number'] = df['Phone_Number'].str.replace('[^a-zA-Z0-9]', '', regex=True)


# First convert the entire column to string's using a lambda function
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))

# Standardizing the phone numbers
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

# Clears out any numbers that have Na or nan
df["Phone_Number"] = df["Phone_Number"].str.replace('nan--', '')
df["Phone_Number"] = df["Phone_Number"].str.replace('Na--', '')

# Here we split the address at every comma, and create new tables called Street Address, State, and Zip Code
df[["Street Address", "State", "Zip Code"]] = df["Address"].str.split(',', expand=True)

# Standardizing the Paying Customer Column (self explanatory)
df["Paying Customer"] = df["Paying Customer"].str.replace('Yes', 'Y')
df["Paying Customer"] = df["Paying Customer"].str.replace('No', 'N')

# Standardizing the Do_Not_Contact Column (self explanatory)
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('Yes', 'Y')
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('No', 'N')

# Filling any values that are None or NaN
df = df.replace('N/a', '')
df = df.fillna('')

# Dropping useless rows that we can not call
for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == 'Y':
        df.drop(x, inplace=True)

# No phone number rows get dropped
for x in df.index:
    if df.loc[x, "Phone_Number"] == '':
        df.drop(x, inplace=True)

# Reset the index of the dataframe
df = df.reset_index(drop=True)

# Drop th address column since we split it up prior to this
df = df.drop("Address", axis=1)

# Sort the Dataframe by the first name
df = df.sort_values(by="First_Name")

print(df)