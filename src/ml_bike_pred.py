import os
import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

PRICE_MAX = 4000

def check_road(size):
    unwanted = ['45cm', '52cm', '54cm', '55cm', '56cm', '57cm']
    if size in unwanted:
        return False
    else:
        return True

def read_data():
    df = pd.read_csv('data/cleaned_data.csv')
    df['Unwanted'] = df['Size'].apply(check_road)
    df = df[df['Unwanted']]
    df = df.drop('Unwanted', axis=1)
    df = df[(df['Currency'] == 'CAD') | (df['Currency'] == 'USD')]
    df = df.drop('Unnamed: 0', axis=1)

    dummies = pd.get_dummies(df['Condition'])
    matierial = pd.get_dummies(df['Material'])
    currency = pd.get_dummies(df['Currency'])
    size = pd.get_dummies(df['Size'])
    df = df.drop('Condition', axis=1)
    df = df.drop('Material', axis=1)
    df = df.drop('Currency', axis=1)
    df = df.drop('Size', axis=1)
    df = pd.concat([df,dummies, size, matierial, currency], axis=1)
    df = df[df['Price'] <= PRICE_MAX]
    df = df[df['Price'] >= 1000]
    return df

def nlp(df=None):
    if  df is None:
        df = pd.read_csv('data/cleaned_data.csv')
    tf_idf = TfidfVectorizer(stop_words='english')
    x= tf_idf.fit_transform(raw_documents=df['Title'])
    
    df = pd.DataFrame(x.toarray())
    return df

    # print(type(vals))
    

def predict():
    df = read_data()
    nlp_df = nlp(df)
    df = df.drop('Title', axis=1)
    df = pd.concat([df, nlp_df])
    df = df.fillna(value=0)
    df = df[df['Price'] >= 1000]
    X = df.drop('Price', axis=1)
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    rf = RandomForestRegressor()
    rf.fit(X=X_train, y=y_train)
    preds = rf.predict(X_test)
    print(sqrt(mean_squared_error(y_true=y_test, y_pred=preds)))
    
    
    make_plot(y_test=y_test, preds=preds)

def make_plot(y_test, preds):
    x = np.linspace(start=0, stop=PRICE_MAX, num=100)
    y = x
    y_pos = x + 500
    y_neg = x - 500
    fig, ax = plt.subplots()
    ax.scatter(y_test, preds)
    ax.plot(x,y, ls= '--')
    ax.plot(x,y_pos, ls= '--')
    ax.plot(x, y_neg, ls='--')
    ax.set_xlabel('Test Values')
    ax.set_ylabel('Preds')
    plt.show()


def predictions_and_plots():
    fp = os.path.join('data', 'cleaned_data.csv')
    df = read_data(fp)
    print(df.columns)
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    rf = RandomForestRegressor()
    rf.fit(X=X_train, y=y_train)
    preds = rf.predict(X_test)
    print(sqrt(mean_squared_error(y_true=y_test, y_pred=preds)))
    make_plot(y_test=y_test,preds=preds)




if __name__ == '__main__':
    # predictions_and_plots()    
    predict()
    # nlp()
    
    
