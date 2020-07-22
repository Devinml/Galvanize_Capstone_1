import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import seaborn as sns
plt.style.use('ggplot')


def get_norm_coef(df):
    mean_df = df['Price'].mean()
    sqrt_df = np.sqrt(len(df['Price']))
    std = (df['Price'].std())/sqrt_df
    return mean_df,std

def normal_dist(mean,std):
    return stats.norm(loc=mean,scale=std)


if __name__=='__main__':
    df_29 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_29.csv')
    df_275 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_275.csv')
   
    mean_29, std_29 = get_norm_coef(df_29)
    mean_275, std_275 = get_norm_coef(df_275)

    norm_29 = normal_dist(mean_29,std_29)
    norm_275 = normal_dist(mean_275,std_275)
    
    x1 = np.linspace(mean_275-6*std_275,mean_275+6*std_275,500)
    x2 = np.linspace(mean_29-6*std_29,mean_29+6*std_29,500)

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(x1,norm_275.pdf(x1),color='red',label='27.5')
    ax.plot(x2,norm_29.pdf(x2),color= 'blue',label='29')
    ax.set_title('Distribution of Bike Value Means Given Wheel Size')
    ax.set_xlabel("Mean Price")
    ax.set_ylabel("Probablility Density Function (Price)")
    ax.set_ylim([-.0005,.018])
    ax.axvline(mean_29,ymax=norm_29.pdf(mean_29)/(.01775),color = 'blue',ls = '--',alpha=.5)
    ax.axvline(mean_275,ymax=norm_275.pdf(mean_275)/(.018),color = 'red',ls = '--',alpha=.5)
    
    ax.set_xticks([2600,
                    round(mean_275-2*std_275,5),
                    round(mean_275,5),
                    round(mean_275+2*std_275,5),
                    round(mean_275+(mean_29-mean_275)/2,5),
                    round(mean_29-2*std_29,5),
                    round(mean_29,5),
                    round(mean_29+2*std_29,5),3600])
    plt.xticks(rotation=35)
    ax.legend()

    fig1,ax1 = plt.subplots(figsize=(12,5))
    sns.distplot(df_275['Price'],color='red',bins=50,kde=True,ax=ax1,label='27.5')
    sns.distplot(df_29['Price'],color='blue',bins=50,kde=True,ax=ax1,label='29')
    
    ax1.legend()

    fig2,ax2 = plt.subplots(figsize=(12,5))
    # sns.kdeplot(x1,df_275['Price'],ax=ax2,label='27.5')
    # sns.kdeplot(x2,df_29['Price'],ax=ax2,label='29')
    sns.distplot(df_275['Price'],color='red',bins=50,kde=False,ax=ax2,label='27.5')
    sns.distplot(df_29['Price'],color='blue',bins=50,kde=False,ax=ax2,label='29')
    ax2.legend()

    plt.tight_layout()
    plt.show()

    
    
