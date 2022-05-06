#!/usr/bin/env python
# coding: utf-8

# # DH Final Project Code

# In[6]:


# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


# In[17]:


df = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_1.csv", header=None)
df = df.rename(columns={0: 'id', 1: 'sentiment'})
df = df.sample(frac=0.05)
for i in range(1, 670) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.rename(columns={0: 'id', 1: 'sentiment'})
        temp = temp.sample(frac=0.05)
        df = pd.concat([df, temp])
    except Exception as e:
        print(e)
        continue
        
df.shape


# -  5% sampling of each file ~17 min runtime (90 million entries)

# ### Finding averages with 2k tweet sample

# In[56]:


avg = []

for i in range(0, 665) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.sample(n=2000)
        avg.append(sum(temp[1])/2000)
        
    except Exception as e:
        print(e)
        continue
        


# In[82]:


plt.figure
x=[i for i in range(len(avg))]
start = datetime.datetime(2020, 3, 18)
dates = [start+datetime.timedelta(days=i) for i in range(len(avg))]
plt.plot(dates, avg)
plt.title("Sentiment over time")
plt.xlabel("Date")
plt.ylabel("Sentiment")
plt.xticks(rotation=90)
plt.savefig("unaveraged_Wzeroes.png")


# In[165]:


avg_no_zeroes = []
std_test = []

for i in range(0, 670) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.sample(n=2000)
        temp = temp[temp[1]!= 0]
        avg_no_zeroes.append(sum(temp[1])/len(temp[1]))
        std_test.append(temp[1].std())
    except Exception as e:
        print(e)
        continue


# In[166]:


upper = np.add(np.array(avg_no_zeroes), np.array(std_test))
lower = np.subtract(np.array(avg_no_zeroes), np.array(std_test))


# In[176]:


plt.figure(figsize=(8,6))
# x=[i for i in range(len(avg))]
# start = datetime.datetime(2020, 3, 18)
# dates = [start+datetime.timedelta(days=i) for i in range(len(avg))]
plt.plot(dates, avg_no_zeroes)
plt.title("Sentiment over time")
plt.xlabel("Date")
plt.ylabel("Sentiment")
plt.xticks(rotation=90)

# TOGGLE this line to get rid of STD filler
# plt.fill_between(dates, upper, lower, alpha = 0.1)


# plt.savefig("figures/unaveraged_no_zeroes_with_sdv.png")


# ### Moving Averages Using DF

# In[200]:


std_div10 = np.array(std_test)/10
df_avg = pd.DataFrame(data={"sentiment":avg_no_zeroes, "date": dates, "sdv": std_div10})
df_avg.head()


# In[201]:


df_avg.iloc[15].sdv


# In[202]:


moving_avg_7day = []
moving_avg_7day_sdv = []

for i in range(0, len(dates), 7) :
    s = 0
    s_sdv = 0
    denom = 7
    first = True
    for j in range(7) :
        try :
            s += df_avg.iloc[i+j].sentiment
            s_sdv += df_avg.iloc[i+j].sdv
        except :
            if first : 
                denom = j+1
                first = False
            continue
    moving_avg_7day.append(s/(denom))
    moving_avg_7day_sdv.append(s_sdv/(denom))

upper = np.add(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))
lower = np.subtract(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))


# In[203]:


plt.figure
dates7day = [start+datetime.timedelta(days=i) for i in range(0,len(avg), 7)]
plt.plot(dates7day, moving_avg_7day)
plt.title("Sentiment Moving Average Weekly With SDV/10")
plt.xlabel("Date")
plt.ylabel("Sentiment")
plt.xticks(rotation=90)
plt.fill_between(dates7day, upper, lower, alpha = 0.1)
# plt.savefig("figures/averaged_no_zeroes_7day_with_sdv.png")


# In[209]:


moving_avg_30day = []
moving_avg_30day_sdv = []

for i in range(0, len(dates), 30) :
    s = 0
    s_sdv = 0
    denom = 30
    first = True
    for j in range(30) :
        try :
            s += df_avg.iloc[i+j].sentiment
            s_sdv += df_avg.iloc[i+j].sdv
        except :
            if first : 
                denom = j+1
                first = False
            continue
            equal = True
    moving_avg_30day.append(s/(denom))
    moving_avg_30day_sdv.append(s_sdv/(denom))

upper = np.add(np.array(moving_avg_30day), np.array(moving_avg_30day_sdv))
lower = np.subtract(np.array(moving_avg_30day), np.array(moving_avg_30day_sdv))


# In[223]:


plt.figure
dates30day = [start+datetime.timedelta(days=i) for i in range(0,len(dates), 30)]
plt.plot(dates30day, moving_avg_30day, 'r')
plt.title("Sentiment Moving Average Monthly with SDV/10")
plt.xlabel("Date")
plt.ylabel("Sentiment")
plt.xticks(rotation=90)
plt.fill_between(dates30day, upper, lower, alpha = 0.1, color='red')
plt.savefig("figures/averaged_no_zeroes_30day.png")


# ### Run with 5 different random samples

# In[9]:


# loop through to create week averaged and month averaged graphs for 5 samples
for k in range(5) :
    avg_no_zeroes_sample = []
    sdv = []
    dates = [start+datetime.timedelta(days=i) for i in range(len(avg))]
    
    # Calculate Avg with no zeroes for all days and STD
    
    for i in range(0, 665) :
        try :
            temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
            temp = temp.sample(n=2000)
            temp = temp[temp[1]!= 0]
            avg_no_zeroes_sample.append(sum(temp[1])/len(temp[1]))
            sdv.append(temp[1].std())
        except Exception as e:
            print(e)
            continue
    
    # Create Average df
    std_div10 = np.array(sdv)/10
    df_avg = pd.DataFrame(data={"sentiment":avg_no_zeroes_sample, "date": dates, "sdv": std_div10})
    
    # Find Moving Averages for plotting
    
    ## 7 day
    moving_avg_7day = []
    moving_avg_7day_sdv = []

    for i in range(0, len(dates), 7) :
        s = 0
        s_sdv = 0
        denom = 7
        first = True
        for j in range(7) :
            try :
                s += df_avg.iloc[i+j].sentiment
                s_sdv += df_avg.iloc[i+j].sdv
            except :
                if first : 
                    denom = j+1
                    first = False
                continue
        moving_avg_7day.append(s/(denom))
        moving_avg_7day_sdv.append(s_sdv/(denom))

    upper_7 = np.add(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))
    lower_7 = np.subtract(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))
        
    ## 30 day
    moving_avg_30day = []
    moving_avg_30day_sdv = []

    for i in range(0, len(dates), 30) :
        s = 0
        s_sdv = 0
        denom = 30
        first = True
        for j in range(30) :
            try :
                s += df_avg.iloc[i+j].sentiment
                s_sdv += df_avg.iloc[i+j].sdv
            except :
                if first : 
                    denom = j+1
                    first = False
                continue
                equal = True
        moving_avg_30day.append(s/(denom))
        moving_avg_30day_sdv.append(s_sdv/(denom))

    upper_30 = np.add(np.array(moving_avg_30day), np.array(moving_avg_30day_sdv))
    lower_30 = np.subtract(np.array(moving_avg_30day), np.array(moving_avg_30day_sdv))
    
    plt.figure(figsize=(8,6))
    dates7day = [start+datetime.timedelta(days=i) for i in range(0,len(dates), 7)]
    plt.plot(dates7day, moving_avg_7day)
    plt.title(f"Sentiment Moving Average Weekly Sample {k}")
    plt.xlabel("Date")
    plt.ylabel("Sentiment")
    plt.xticks(rotation=90)
    plt.fill_between(dates7day, upper_7, lower_7, alpha = 0.1)
#     plt.savefig(f"figures/samples_2k/averaged_no_zeroes_7day_{k}.png")
    
    dates30day = [start+datetime.timedelta(days=i) for i in range(0,len(dates), 30)]
    plt.plot(dates30day, moving_avg_30day, 'r')
    plt.title(f"Sentiment Moving Average Monthly Sample {k+1}")
    plt.xlabel("Date")
    plt.ylabel("Sentiment")
    plt.xticks(rotation=90)
#     plt.fill_between(dates30day, upper_30, lower_30, alpha = 0.1, color='red')
    plt.savefig(f"figures/samples_2k/averaged_no_zeroes_30day_{k+1}.png")
    


# In[12]:


get_ipython().system('brew reinstall twarc')

