#!/usr/bin/env python
# coding: utf-8

# # Weather forecast SMS sending

# ## Websites

# Twilio: https://www.twilio.com/en-us

# Weather API: https://www.weatherapi.com/

# ### Twilio tokens:

# ###### Account SID:

# AC33ae0ed26f623a42d5767445994807cf

# ###### Auth Token:

# c33ae12852e70b97e3078b68fc8de318

# ###### Twilio Phone Number:

# +12138141175

# #### API KEY WAPI

# 7539a2278a864643bac71600230810

# ## Install libraries

# ###### Request:
# conda install -c anaconda requests

# ###### Twilio:
# conda install -c conda-forge twilio

# ## Inport libraries

# In[1]:


import os
from twilio.rest import Client
import requests
import requests.exceptions
import json
import pandas as pd
import bs4
import datetime


# ## URL

# In[5]:


query='Mexico city'
api_key = '7539a2278a864643bac71600230810'
url_weather= "http://api.weatherapi.com/v1/forecast.json?key=" + api_key + "&q="+ query +"&days=1&aqi=no&alerts=no"


# ## Request

# In[6]:


response= requests.get(url_weather).json()


# ##### NOTE:
# Print the response in order to look for the information we need

# In[7]:


response


# ## Keys

# In[8]:


response.keys()


# ###### NOTE:
# We'll use the 'forecast' key

# In[9]:


response['forecast']


# ###### NOTE: 
# Since it only has one position we'll the position 0 and look for the keys

# In[10]:


response['forecast']['forecastday'][0].keys()


# ##### NOTE:
# We only need the quantity of hours in a day 

# In[11]:


len(response['forecast']['forecastday'][0]['hour'])


# ##### NOTE:
# We already know the quantity of hours in a day so randomly we will pick one position in order to know what information has on it

# In[12]:


response['forecast']['forecastday'][0]['hour'][1]


# ##### NOTE:
# We already know that we will need to use the key 'time' so we print it to read the information on it

# In[13]:


response['forecast']['forecastday'][0]['hour'][1]['time']


# ##### NOTE:
# Since it has an empty space we will split the value in two pieces an print the first part to obtain the date

# In[14]:


response['forecast']['forecastday'][0]['hour'][1]['time'].split()[0]


# ##### NOTE:
# We do the same with the second part of the value to obtain the hour

# In[15]:


response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1]


# ##### NOTE:
# We split the hour and the minute and convert the value into an integer

# In[16]:


int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0])


# ##### NOTE:
# We will look for the key hour in order to know the condition at that specific time

# In[17]:


response['forecast']['forecastday'][0]['hour'][0]


# In[18]:


response['forecast']['forecastday'][0]['hour'][0].keys()


# ##### NOTE:
# We will use the key 'condition' to obtain the information we are looking for

# In[19]:


response['forecast']['forecastday'][0]['hour'][0]['condition']


# ##### NOTE:
# We will only use the key 'text'

# In[20]:


response['forecast']['forecastday'][0]['hour'][0]['condition']['text']


# ##### NOTE:
# The next step is look for the temperature in °C

# In[21]:


response['forecast']['forecastday'][0]['hour'][0]['temp_c']


# ##### NOTE:
# Then we will look for if the it will rain that day. (0=NO, 1=YES)

# In[22]:


response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']


# ##### NOTE:
# Finally we will look for the chance of rain that day in %

# In[23]:


response['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']


# ## Dataframe

# ##### NOTE:
# We will write a function and assign a variable to each breakdown key that we will use but replacing the hour with an variable (in this case 'i')

# In[24]:


def get_forecast(response,i):
    date = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hour = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condition = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temp = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    chance_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return date,hour,condition,temp,rain,chance_rain


# ##### NOTE:
# we will create an empty list and write a for loop (if we already know the length we can you write it) and apply the function to each element

# In[25]:


data = []
for i in range(len(response['forecast']['forecastday'][0]['hour'])):
    data.append(get_forecast(response,i))   


# In[26]:


data


# ##### NOTE: 
# Create the data frame

# In[27]:


col = ['date','hour','condition','temp','rain','chance_rain']
df = pd.DataFrame(data,columns = col)


# In[28]:


df


# ##### NOTE:
# Filter the information
# We want just the information of the days that will rain and the possible hours when the user is outside

# In[29]:


df_rain = df[(df['rain'] == 1) & (df['hour'] > 6) & (df['hour'] < 23)]
df_rain = df_rain[['hour','condition']]
df_rain.set_index('hour',inplace = True)


# In[30]:


df_rain


# ## Message template

# In[31]:


message_template = "\nHello \n\n The weather today " +df["date"][0] + " in " + query + " is \n\n" + str(df_rain) 


# In[32]:


message_template


# ### Phone number

# In[34]:


phone_number = '+12138141175'


# In[35]:


phone_number


# ### SMS via Twilio

# ##### NOTE:
# copy and paste the template from the link: https://www.twilio.com/docs/messaging/tutorials/how-to-send-sms-messages/python#maincontent replacing the data with your data

# In[42]:


#### account_sid = 'AC33ae0ed26f623a42d5767445994807cf'
auth_token = 'c33ae12852e70b97e3078b68fc8de318'

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body= message_template,
         from_= phone_number,
         to='+524181709157'
     )

print('Message sent' + message.sid)

