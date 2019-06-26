#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset (noshowappointments- data set!)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>
# 
# 
# 
# 

# <a id='intro'></a>
# ## Introduction
# 
# 

# >This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row.
# ScheduledDay, tells us on what day the patient set up their appointment.
# ‘Neighborhood’ indicates the location of the hospital.
# ‘Scholarship’ indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família.
# the data set is provided by kaggel.
# throughout this project we are trying to answer these questions by exploring the dataset and also the connections among variables.
# 
# 
# 

# 
# ## Questions:
# >(1)Are patient who missed an appointmant befor more likly to miss the next appointment?
# (2)What is the no-show proportion?
# (3)Are no-show appointments associated with a certain gender?
# (4)How are weekdays affecting patients absence?
# (5)How is age affecting patients absence?

# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# ### General Properties

# In[411]:


#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
df=pd.read_csv('noshowappointments.csv')#open data st
df.head(10)#exploring the data


# > In order to understand the dataset we will call shape, info and describe.

# In[412]:


df.shape


# > So, we have 110527 appoinmements were booked and 14 columns.

# In[413]:


df.info()


# In[414]:


df.describe()


# > We could see that the min age is -1 which is impossible!
# and no null values in all 14 coulmns, How lucky we are :)
# all columns type are okay but for AppointmentDay and ScheduledDay columns we will change it to datetime.

# In[415]:


df.duplicated().sum()


# > No duplicated rows in the data set.

# In[416]:


df.isnull().sum()


# > No null values in the data set.

# 
# ### Data Cleaning 

# In[417]:


#changing data type and column name 
df.rename(columns={'No-show':'NoShow'},inplace=True)
# declaring a function 
def changeToTime (c):
    df[c]=pd.to_datetime(df[c])
    
# calling the function    
changeToTime('AppointmentDay') 
changeToTime('ScheduledDay')


df['hour_scheduled']=df['ScheduledDay'].dt.hour

df['day_scheduled']=df['ScheduledDay'].dt.weekday_name
df['day_appointment']=df['AppointmentDay'].dt.weekday_name

df.info()


# > We have created a function ( changeToTime) to change AppointmentDay datatype and ScheduledDay to datetime64[ns].And change the No-show column to NoShow cause I have got a problem each time I deal with. Also I add new colunms hour_scheduled,day_scheduled, day_appointment where they determine the hour of scheduled, week day name of ScheduledDay and week day name of AppointmentDay ,respectively. 
# 
# 

# In[418]:


df.query('Age == -1')


# In[419]:


df.drop(99832,axis=0,inplace=True)
df.describe()


# In[420]:


df.shape


# > We have deleted the row where -1 value in age.

# In[421]:


df.replace(('Yes', 'No'), (1, 0), inplace=True)


# > To make the data more Understandable and easy to deal with, We have changed the No, yes values in the data set to 0,1.

# In[422]:


df['AppointmentsMissed'] =df.groupby('PatientId')['NoShow'].apply(lambda x: x.cumsum())

df.query('AppointmentsMissed > 1 ')


# > We have added a new column AppointmentsMissed which sums how many has the patient been absent.
# I would like to see if there is a relation between NoShow and AppointmentsMissed.

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1 (Are patient who missed an appointmant befor more likly to miss the next appointment?)

# In[423]:


df.corr()


# > Since the correlation is 0.58 , that means there is a possitive relationship between NoShow and AppointmentsMissed 

# ### Research Question 2 (What is the no-show proportion?)

# In[424]:


# yes means patient no show, No means patient show.
df['NoShow'].value_counts()
df_yes=df.query('NoShow == 1')
df_no=df.query('NoShow == 0')
ff1=(df_yes.shape[0]/df.shape[0])*100 # no show percentage
ff2=(df_no.shape[0]/df.shape[0])*100 # no show percentage


labels = ['no show', 'show']
sizes = [ff1, ff2]
explode = (0.1,0) # only "explode" the 1st slice 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal') 
plt.title('NoShow Proportion')
plt.show()



# > 20.2% of appointments were missed.

# ### Research Question 3 (Are no-show appointments associated with a certain gender?)

# In[425]:



female_prop=df_yes.query('Gender =="F"')
male_prop=df_yes.query('Gender =="M"')
g1=female_prop.shape[0]/df_yes.shape[0]
g2=male_prop.shape[0]/df_yes.shape[0]
labels = 'F','M'
sizes = [g1,g2]
explode = (0.1,0) # only "explode" the 1st slice 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal') 
plt.title('Absent patients Gender Proportion')
plt.show()


# >As shown in the plot , Female are more expected to not show with proportion 65.4%
# That is maybe because of their busy life.

# ### Research Question 4  ( How are weekdays affecting patients absence?)

# In[426]:


m=df_yes.day_appointment.value_counts()/df.day_appointment.value_counts()
#plt.bar(m.index,m)


y_pos = np.arange(len(m.index))

 
plt.bar(y_pos, m, align='center', alpha=0.5)
plt.xticks(y_pos, m.index)
plt.xlabel('Day')
plt.ylabel('Proportion')
plt.title('Days Proportion for Not coming ')
 
plt.show()


# > As shown in the plot, Saturday is more likely to has not coming patients.
# And I think that because Saturday is weekend where people used to have a plan, or to relax at home.

# ### Research Question 5  ( How is age affecting patients absence?)

# In[427]:


x = df_yes['Age']
num_bins = 15
n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Age')
plt.ylabel('frequency')
plt.title(' Age frequency of Absent patients ')
plt.show()


# >Clearly , the more Age is increasing the less likly that patient will be absent. 

# <a id='conclusions'></a>
# ## Conclusions
# 
# 

# > noshowappointments data set is very interesting, it has alot of columns that all contribute to affect the NoShow situation.I did alot of wrangling such as ( adding columns, deleting rows, rename columns, changing datatype of columns). I tried to see How ( Gender, Age,weekday, AppointmentsMissed) will affect the patient absence.Then I plot a visuals to show results.
# to conclude, There are alot of  factors affect NoShow situation, some of them are age, gender, week day, how many AppointmentsMissed. although there are more factors also affect NoShow we have not discussed here.
