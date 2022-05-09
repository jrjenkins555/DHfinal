#!/usr/bin/env python
# coding: utf-8

# # DH Final Project Code

# In[19]:


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


# In[18]:


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
    


# ## Initial Spike Analysis

# In[38]:


avg_no_zeroes_first_spike = []
std_test = []

for i in range(1, 119) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.sample(n=2000)
        temp = temp[temp[1]!= 0]
        avg_no_zeroes_first_spike.append(sum(temp[1])/len(temp[1]))
        std_test.append(temp[1].std())
    except Exception as e:
        print(e)
        continue
        
startSpike = datetime.datetime(2020, 3, 21)
datesFirstSpike = [startSpike+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_first_spike))]
dates7daySpike = [startSpike+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_first_spike), 7)]


# In[39]:


std_div10 = np.array(std_test)/10
df_avg_spike = pd.DataFrame(data={"sentiment":avg_no_zeroes_first_spike, "date": datesFirstSpike, "sdv": std_div10})
df_avg_spike.head()


# In[40]:


moving_avg_7day_firstSpike = []
moving_avg_7day_sdv_firstSpike = []

for i in range(0, len(avg_no_zeroes_first_spike), 7) :
    s = 0
    s_sdv = 0
    denom = 7
    first = True
    for j in range(7) :
        try :
            s += df_avg_spike.iloc[i+j].sentiment
            s_sdv += df_avg_spike.iloc[i+j].sdv
        except :
            if first : 
                denom = j+1
                first = False
            continue
    moving_avg_7day_firstSpike.append(s/(denom))
    moving_avg_7day_sdv_firstSpike.append(s_sdv/(denom))

# upper = np.add(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))
# lower = np.subtract(np.array(moving_avg_7day), np.array(moving_avg_7day_sdv))


# In[73]:


# 4 = March 21
# 119 = July 15
plt.figure(figsize=(10,8))
plt.plot(datesFirstSpike, avg_no_zeroes_first_spike)
plt.plot(dates7daySpike, moving_avg_7day_firstSpike, 'r')

plt.axvline(x = datetime.datetime(2020,7,7), color='g',label = '3 million cases reached', linestyle='dotted')
plt.axvline(x = datetime.datetime(2020,5,12), color='c',label = 'Fauci states 80k deaths are underestimated',linestyle='dotted')
plt.axvline(x = datetime.datetime(2020,3,26), color='k',label = 'Senate Passes CARES act', linestyle='dotted')


plt.title("First Spike Sentiment Scores")
plt.xlabel("Date")
plt.ylabel("Sentiment")
plt.xticks(rotation=90)
plt.legend()

plt.savefig("figures/spike/initial.png")


# In[84]:


cases = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/national-history.csv")
casesFirstSpike = cases.iloc[len(cases)-len(datesFirstSpike)-1:len(cases)-1]
casesFirstSpike = casesFirstSpike[["date", "positiveIncrease"]]


# In[131]:


fig, ax1 = plt.subplots(figsize=(10,8))

ax1.plot(datesFirstSpike, avg_no_zeroes_first_spike, label="Sentiment")
ax1.plot(dates7daySpike, moving_avg_7day_firstSpike, 'r', label = "Sentiment weekly avg")

ax2 = ax1.twinx()
ax2.plot(datesFirstSpike, casesFirstSpike.positiveIncrease, 'm', label = "Cases")

ax1.set_title("First Spike Sentiment with Case Counts")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sentiment")
ax2.set_ylabel("Case Counts")
ax1.tick_params(labelrotation=90)

ax1.legend()
ax2.legend(loc='upper left')

plt.savefig("figures/spike/withCaseCounts")


# ## End 2020 Analysis

# In[133]:


avg_no_zeroes_end_2020 = []
std_test = []

for i in range(271, 347) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.sample(n=2000)
        temp = temp[temp[1]!= 0]
        avg_no_zeroes_end_2020.append(sum(temp[1])/len(temp[1]))
        std_test.append(temp[1].std())
    except Exception as e:
        print(e)
        continue
        
start_end2020 = datetime.datetime(2020, 12, 15)
datesEnd2020 = [start_end2020+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_end_2020))]
dates7dayEnd = [start_end2020+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_end_2020), 7)]


# In[134]:


std_div10 = np.array(std_test)/10
df_avg_end = pd.DataFrame(data={"sentiment":avg_no_zeroes_end_2020, "date": datesEnd2020, "sdv": std_div10})
df_avg_end.head()


# In[135]:


moving_avg_7day_end2020 = []
moving_avg_7day_sdv_end2020 = []

for i in range(0, len(avg_no_zeroes_end_2020), 7) :
    s = 0
    s_sdv = 0
    denom = 7
    first = True
    for j in range(7) :
        try :
            s += df_avg_end.iloc[i+j].sentiment
            s_sdv += df_avg_end.iloc[i+j].sdv
        except :
            if first : 
                denom = j+1
                first = False
            continue
    moving_avg_7day_end2020.append(s/(denom))
    moving_avg_7day_sdv_end2020.append(s_sdv/(denom))


# In[136]:


cases_1 = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/national-history_1.csv")
casesEnd2020 = cases_1.iloc[len(cases_1)-len(datesEnd2020)-1:len(cases_1)-1]
casesEnd2020 = casesEnd2020[["date", "positiveIncrease"]]


# In[137]:


fig, ax1 = plt.subplots(figsize=(10,8))

ax1.plot(datesEnd2020, avg_no_zeroes_end_2020, label='Sentiment')
ax1.plot(dates7dayEnd, moving_avg_7day_end2020, 'r', label="Sentiment weekly avg")

ax2 = ax1.twinx()
ax2.plot(datesEnd2020, casesEnd2020.positiveIncrease, 'm', label="Cases")

ax1.set_title("End of 2020 Sentiment with Case Counts")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sentiment")
ax2.set_ylabel("Case Counts")
ax1.tick_params(labelrotation=90)

ax1.legend(loc='lower right')
ax2.legend(loc='upper right')

plt.savefig("figures/end2020/withCaseCounts")


# In[140]:


fig, ax1 = plt.subplots(figsize=(10,8))

ax1.plot(dates7dayEnd, moving_avg_7day_end2020, 'r', label="Sentiment weekly avg")

ax2 = ax1.twinx()
ax2.plot(datesEnd2020, casesEnd2020.positiveIncrease, 'm', label="Cases")

ax1.axvline(x = datetime.datetime(2021,1,20), color='g',label = 'Biden Inauguration', linestyle='dotted')
ax1.axvline(x = datetime.datetime(2020,12,28), color='b',label = 'FDA approves new tests and vaccines', linestyle='dotted')

ax1.set_title("End of 2020 Sentiment with Notable Events")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sentiment")
ax2.set_ylabel("Case Counts")
ax1.tick_params(labelrotation=90)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig("figures/end2020/events")


# ## Omicron Announced

# In[174]:


avg_no_zeroes_omi = []
std_test = []

for i in range(593, 668) :
    try :
        temp = pd.read_csv(filepath_or_buffer=f"/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_{i+1}.csv", header=None)
        temp = temp.sample(n=2000)
        temp = temp[temp[1]!= 0]
        avg_no_zeroes_omi.append(sum(temp[1])/len(temp[1]))
        std_test.append(temp[1].std())
    except Exception as e:
        print(e)
        continue
        
start_omi = datetime.datetime(2021, 11, 1)
datesOmi = [start_omi+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_omi))]
dates7dayOmi = [start_omi+datetime.timedelta(days=i) for i in range(0,len(avg_no_zeroes_omi), 7)]


# In[175]:


std_div10 = np.array(std_test)/10
df_avg_omi = pd.DataFrame(data={"sentiment":avg_no_zeroes_omi, "date": datesOmi, "sdv": std_div10})
df_avg_omi.head()


# In[176]:


moving_avg_7day_omi = []
moving_avg_7day_sdv_omi = []

for i in range(0, len(avg_no_zeroes_omi), 7) :
    s = 0
    s_sdv = 0
    denom = 7
    first = True
    for j in range(7) :
        try :
            s += df_avg_omi.iloc[i+j].sentiment
            s_sdv += df_avg_omi.iloc[i+j].sdv
        except :
            if first : 
                denom = j+1
                first = False
            continue
    moving_avg_7day_omi.append(s/(denom))
    moving_avg_7day_sdv_omi.append(s_sdv/(denom))


# In[177]:


cases_omi = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/us.csv")
cases_omi = cases_omi.iloc[len(cases_omi)-len(datesOmi)-1:len(cases_omi)-1]
cases_omi = cases_omi[["date", "cases"]]


# In[178]:


fig, ax1 = plt.subplots(figsize=(10,8))

# ax1.plot(datesOmi, avg_no_zeroes_omi, label='Sentiment')
ax1.plot(dates7dayOmi, moving_avg_7day_omi, 'r', label="Sentiment weekly avg")

ax2 = ax1.twinx()
ax2.plot(datesOmi, cases_omi.cases, 'm', label="Cumulative cases")

ax1.axvline(x = datetime.datetime(2021,11,26), color='g',label = 'Omicron Variant Announced', linestyle='dotted')
ax1.axvline(x = datetime.datetime(2021,12,20), color='b',label = 'CDC warns of rapid increase in cases', linestyle='dotted')

ax1.set_title("Omicron Era Sentiment with Notable Events")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sentiment")
ax2.set_ylabel("Cumulatice Case Count")
ax1.tick_params(labelrotation=90)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig("figures/omicron/events.png")

