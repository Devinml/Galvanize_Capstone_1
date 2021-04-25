import os
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def check_road(size):
    unwanted = ['45cm', '52cm', '54cm', '55cm', '56cm', '57cm']
    if size in unwanted:
        return False
    else:
        return True

def read_data(fp):
    df = pd.read_csv('data/cleaned_data.csv')
    df['Unwanted'] = df['Size'].apply(check_road)
    df = df[df['Unwanted']]
    df = df.drop('Unwanted', axis=1)
    df = df[(df['Currency'] == 'CAD') | (df['Currency'] == 'USD')]
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop('Title', axis=1)
    
    
    dummies = pd.get_dummies(df['Condition'])
    matierial = pd.get_dummies(df['Material'])
    currency = pd.get_dummies(df['Currency'])
    size = pd.get_dummies(df['Size'])
    df = df.drop('Condition', axis=1)
    df = df.drop('Material', axis=1)
    df = df.drop('Currency', axis=1)
    df = df.drop('Size', axis=1)
    df = pd.concat([df,dummies, size, matierial, currency], axis=1)
    df = df[df['Price'] <= 5000]
    df = df[df['Price'] >= 1000]
    return df

def predictions_and_plots():
    fp = os.path.join('data', 'cleaned_data.csv')
    df = read_data(fp)
    print(df.columns)
    X = df.drop('Price', axis=1)
    y = df['Price']
    print(df.head())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    rf = RandomForestRegressor()
    rf.fit(X=X_train, y=y_train)
    preds = rf.predict(X_test)
    print(sqrt(mean_squared_error(y_true=y_test, y_pred=preds)))

    fig, ax = plt.subplots()
    ax.scatter(y_test, preds)
    ax.set_xlabel('Test Values')
    ax.set_ylabel('Preds')
    plt.show()


if __name__ == '__main__':
    predictions_and_plots()    

    
    
