import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
plt.style.use('ggplot')

df_29 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_29.csv')
df_275 = pd.read_csv('/home/devin/Documents/Galvanize/repos/Galvanize_Capstone_1/data/cleaned_data_275.csv')

def get_norm_coef(df):
    mean_df = df['Price'].mean()
    sqrt_df = np.sqrt(len(df['Price']))
    std_df = df


mean_29 = df_29['Price'].mean()
mean_275 = df_275['Price'].mean()


sqrt_n_29 = np.sqrt(len(df_29['Price']))
sqrt_n_275 = np.sqrt(len(df_275['Price']))

std_29 = (df_29['Price'].std())/sqrt_n_29
std_275 = df_275['Price'].std()/sqrt_n_275

x = np.linspace(2000,4000,2000)

norm_29 = stats.norm(loc=mean_29,scale=std_29)
norm_275 = stats.norm(loc=mean_275,scale=std_275)

fig, ax = plt.subplots()

ax.plot(x,norm_275.pdf(x),color='red')
ax.plot(x,norm_29.pdf(x),color= 'blue')

plt.show()

