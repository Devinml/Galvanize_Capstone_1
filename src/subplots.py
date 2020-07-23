import matplotlib.pyplot as plt
import pandas as pd 









if __name__=='__main__':
    df_29 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_29.csv')
    df_275 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_275.csv')
    df = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data.csv')
    df['Material'] = df['Material'].apply(fix_aluminum_spelling)
    df_29['Material'] = df_29['Material'].apply(fix_aluminum_spelling)
    df_275['Material'] = df_275['Material'].apply(fix_aluminum_spelling)