import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import seaborn as sns
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 16})
import scipy.stats as stats
# from matplotlib.colors import ListedColormap

# # construct cmap
# flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
# my_cmap = ListedColormap(sns.color_palette(flatui).as_hex())


def get_norm_coef(df):
    mean_df = df['Price'].mean()
    sqrt_df = np.sqrt(len(df['Price']))
    std = (df['Price'].std())/sqrt_df
    return mean_df,std

def normal_dist(mean,std):
    return stats.norm(loc=mean,scale=std)

def box_plot_df(df):
    greater_90 = df['Front_travel']>90
    less_than200 = df['Front_travel']<=200
    price_gr_0 = df['Price']>100
    not_75 = df['Front_travel']!=175
    return df[(greater_90)&(less_than200)&(price_gr_0)&(not_75)]


if __name__=='__main__':
    df_29 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_29.csv')
    df_275 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_275.csv')
    df = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data.csv')
   
    mean_29, std_29 = get_norm_coef(df_29)
    mean_275, std_275 = get_norm_coef(df_275)

    norm_29 = normal_dist(mean_29,std_29)
    norm_275 = normal_dist(mean_275,std_275)
    
    x1 = np.linspace(mean_275-6*std_275,mean_275+6*std_275,500)
    x2 = np.linspace(mean_29-6*std_29,mean_29+6*std_29,500)

    t_test = stats.ttest_ind(df_29['Price'],df_275['Price'],equal_var=False)
    fig, ax = plt.subplots(figsize=(12,8))

    ax.plot(x1,norm_275.pdf(x1),color='#C95948',label='27.5')
    ax.plot(x2,norm_29.pdf(x2),color= '#4586AC',label='29')
    # sns.lineplot(x=x1,y=norm_275.pdf(x1),color='tab:red',ax=ax,label='27.5')
    # sns.lineplot(x=x2,y=norm_29.pdf(x2),color='tab:blue',ax=ax,label='29')
    ax.set_title('Distribution of Bike Value Means Given Wheel Size')
    ax.set_xlabel("Mean Price")
    ax.set_ylabel("Probablility Density Function (Price)")
    ax.set_ylim([-.0005,.018])
    ax.axvline(mean_29,ymax=norm_29.pdf(mean_29)/(.01775),color = '#4586AC',ls = '--',alpha=.5)
    ax.axvline(mean_275,ymax=norm_275.pdf(mean_275)/(.018),color = '#C95948',ls = '--',alpha=.5)
    plt.text(3225,0.0143594,s=f'T_stat = {t_test[0]:.2f}, p value = {t_test[1]:.2f}')
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
    sns.distplot(df_275['Price'],color='#4586AC',bins=50,kde=True,ax=ax1,label='27.5')
    sns.distplot(df_29['Price'],color='#C95948',bins=50,kde=True,ax=ax1,label='29')
    ax1.set_title('Histogram of 27.5" and 29" Wheel Bikes')
    ax1.legend()
    
   

    fig2,ax2 = plt.subplots(figsize=(12,5))
    bins_ = [i for i in range(0,10000,150)]
   
    sns.distplot(df_275['Price'],color='#C95948',bins=bins_,kde=False,ax=ax2,label='27.5')
    sns.distplot(df_29['Price'],color='#4586AC',bins=bins_,kde=False,ax=ax2,label='29')
    

    ax2.set_xticks(np.linspace(0,10000,25))
    ax2.set_title('Histogram of 27.5" and 29" Wheel Bikes')
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Price')
    ax2.legend()
    plt.xticks(rotation=35)
    
    fig3,ax3 = plt.subplots(figsize=(12,5))
    sns.boxplot(x='Front_travel',y='Price',data = box_plot_df(df),hue="Wheel_Size",ax=ax3)
    ax3.set_xlabel('Front Travel')


    fig4,ax4 = plt.subplots(figsize=(7,9))
    sns.boxplot(x='Material',y='Price',data=df)
    plt.tight_layout()
    plt.show()

    
    
