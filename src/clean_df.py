import pandas as pd


def Check_Material(string):
    #cleans the df by filtering material
    if string == 'Aluminium' or string == 'Carbon Fiber' or string == 'Chromoly' or string== 'Steel' or string =='Titanium':
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
    #convert string to float
    nums = '1234567890.'
    string = ''
    for char in input_string:
        if char in nums:
            string+= char
    return float(string)

def rear_travel_clean(x):
    # remove rows that contain travel in the rear travel
    if x =="Travel:":
        return False
    else:
        return True

def clean_df1(df1):
    #drop axis made from bad data
    df1.drop(axis = 1,labels = 'Unnamed: 9',inplace=True)
    #check to make sure the frame material is a correct value
    df1 = df1[df1['Material'].apply(lambda x : Check_Material(x))].copy()
    #convert the wheel size from string to float
    df1['Wheel_Size'] = df1['Wheel_Size'].apply(lambda x : convert_wheel_string(x))
    #convert string of front travel to float
    df1['Front_travel'] = df1['Front_travel'].apply(convert_string_flt)
    #convert string of rear travel to float and remove bad values
    df1 = df1[df1['Rear_travel'].apply(rear_travel_clean)]
    df1['Rear_travel'] = df1['Rear_travel'].apply(convert_string_flt)
    #make price a float
    df1['Price'] = df1['Price'].apply(convert_string_flt)
    #complete curr. convert
    
    #return DF




if __name__=='__main__':
    # Read in CSV files into DF
    df1 = pd.read_csv('../data/data_work.csv')
    df2 = pd.read_csv('../data/data_work_2.csv')
    # clean DF1 
    df1.drop(axis = 1,labels = 'Unnamed: 9',inplace=True)
    df1 = df1[df1['Material'].apply(lambda x : Check_Material(x))].copy()
    df1['Wheel_Size'] = df1['Wheel_Size'].apply(lambda x : convert_wheel_string(x))
    df1['Front_travel'] = df1['Front_travel'].apply(convert_string_flt)
    df1 = df1[df1['Rear_travel'].apply(rear_travel_clean)]
    df1['Rear_travel'] = df1['Rear_travel'].apply(convert_string_flt)
    df1['Price'] = df1['Price'].apply(convert_string_flt)
    #clean 2nd data frame


    # join the two dataframes

