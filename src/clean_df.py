import pandas as pd


def check_material(string):
    # Cleans the df by filtering material
    if string == 'Aluminium' or string == 'Carbon Fiber':
        return True
    elif string == 'Chromoly' or string == 'Steel':
        return True
    elif string == 'Titanium':
        return True
    else:
        return False


def convert_wheel_string(input_string):
    # change string of wheel to int
    if input_string == '29"':
        return 29
    elif input_string == '27.5"':
        return 27.5


def convert_string_flt(input_string):
    # convert string to float
    nums = '1234567890.'
    string = ''
    for char in input_string:
        if char in nums:
            string += char
    return float(string)


def rear_travel_clean(x):
    # remove rows that contain travel in the rear travel
    if x == "Travel:":
        return False
    else:
        return True


def check_currancy(price, currancy, exch_rate=.74):
    # Convert Currencty from CAD to US
    if currancy == 'CAD':
        return price * exch_rate
    else:
        return price


def clean_df1(df1):
    # Drop axis made from bad data Remove any wrong wheel sizes.
    # Convert Front suspension to float. Convert Rear travel to float and clean
    # Convert Price to float and convert to US $
    df1.drop(axis=1, labels='Unnamed: 9', inplace=True)
    df1 = df1[df1['Material'].apply(lambda x: check_material(x))].copy()
    df1['Wheel_Size'] = df1['Wheel_Size'].apply(lambda x:
                                                convert_wheel_string(x))
    df1['Front_travel'] = df1['Front_travel'].apply(convert_string_flt)
    df1 = df1[df1['Rear_travel'].apply(rear_travel_clean)]
    df1['Rear_travel'] = df1['Rear_travel'].apply(convert_string_flt)
    df1['Price'] = df1['Price'].apply(convert_string_flt)
    df1["Price"] = df1[['Price',
                        'Currance']].apply(
                         lambda x: check_currancy(x.Price, x. Currance),
                         axis=1)
    return df1


def clean_wheel_size_df2(string):
    # Convert string to float of wheel size
    if string == '29':
        return 29.0
    elif string == '275  650B':
        return 27.5
    else:
        return string


def return_curr(string):
    # Return the Correct Currency
    if 'USD' in string:
        return 'USD'
    elif 'CAD' in string:
        return 'CAD'


def remove_other_wheels(obj):
    # Remove other wheels that might be in data
    # That weren't filtered
    if type(obj) == float:
        return True
    else:
        return False


def remove_resonable_trades(input_string):
    # Remove the string Resonable trades accepted
    if 'CAD' in input_string or 'USD' in input_string:
        return True
    else:
        return False


def clean_df2(df2):
    # apply the above functions to df2
    # df2 was data previously scrapped and has sperate issues
    df2['Wheel Size'] = df2["Wheel Size"].apply(clean_wheel_size_df2)
    df2['Front Travel'] = df2['Front Travel'].apply(convert_string_flt)
    df2['Rear Travel'] = df2['Rear Travel'].apply(convert_string_flt)
    df2['Currance'] = df2['Price'].apply(return_curr)
    df2 = df2[df2['Wheel Size'].apply(remove_other_wheels)]
    df2 = df2[df2['Price'].apply(lambda x: remove_resonable_trades(x))]
    df2['Price'] = df2['Price'].apply(convert_string_flt)
    df2['Price'] = df2[['Price',
                        'Currance']].apply(
                         lambda x: check_currancy(x['Price'], x['Currance']),
                         axis=1)
    return df2


if __name__ == '__main__':
    # Read in CSV files into DF

    df1 = pd.read_csv('''/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/data_work.csv''')
    df2 = pd.read_csv('''/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/data_work_2.csv''')
    # clean DF1
    cleaned_df1 = clean_df1(df1)
    # clean DF2
    cleaned_df2 = clean_df2(df2)
    cleaned_df2.rename(columns={'Frame Size': 'Size',
                                'Wheel Size': 'Wheel_Size',
                                'Front Travel': 'Front_travel',
                                'Rear Travel': 'Rear_travel',
                                'Currance': 'Currency'},
                       inplace=True)
    cleaned_df1.rename(columns={'Currance': 'Currency'}, inplace=True)
    # join the two dataframes
    df = pd.concat([cleaned_df1, cleaned_df2])
    df = df[df['Price'] < 12000]
    # Kept seperated for ease of plotting
    df_29 = df[df['Wheel_Size'] == 29]
    df_275 = df[df['Wheel_Size'] == 27.5]
    # Write cleaned data to file
    df_29.to_csv('''/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_29.csv''')
    df_275.to_csv('''/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_275.csv''')
    df.to_csv('''/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data.csv''')
