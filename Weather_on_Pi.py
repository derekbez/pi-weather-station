#!/usr/bin/env python
# coding: utf-8

# In[296]:


from sqlalchemy import create_engine
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# In[297]:


sqlEngine = create_engine('mysql+pymysql://piremote:Password1@192.168.1.100/weather', pool_recycle=3600)


# In[298]:


dbConnection = sqlEngine.connect()


# In[299]:


df = pd.read_sql("select * from WEATHER_MEASUREMENT order by CREATED asc;", dbConnection)


# In[300]:


pd.set_option('display.expand_frame_repr', False)
#print(df)


# In[301]:


df = df[['CREATED','AMBIENT_TEMPERATURE','GROUND_TEMPERATURE','AIR_PRESSURE','HUMIDITY']]
df.head()


# In[302]:


df['GROUND_TEMPERATURE'].mask(df['GROUND_TEMPERATURE'] == -255, inplace=True )


# https://pandas.pydata.org/pandas-docs/stable/search.html?q=to_period
# https://www.interviewqs.com/ddi_code_snippets/extract_month_year_pandas
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.PeriodIndex.html#pandas.PeriodIndex

# In[303]:


df = df.rename(columns={'AMBIENT_TEMPERATURE':'Internal_Temp', 'GROUND_TEMPERATURE':'External_Temp', 'AIR_PRESSURE':'Pressure', 'HUMIDITY':'Humidity'})


# In[304]:


df.plot(x='CREATED',y=['Internal_Temp','External_Temp'])
df.plot(x='CREATED',y=['Humidity'])
df.plot(x='CREATED',y=['Pressure'])
plt.show()


# In[305]:


df['year'] = pd.DatetimeIndex(df['CREATED']).year
df['year_month'] = pd.to_datetime(df['CREATED']).dt.to_period('M')
df['year_month_day'] = pd.to_datetime(df['CREATED']).dt.to_period('D')
df['year_month_day_hour'] = pd.to_datetime(df['CREATED']).dt.to_period('H')
df.head()
print(df)

# In[306]:


df.describe()


# In[307]:


tempIn = df[['CREATED','Internal_Temp','year_month_day']]
tempInMin = tempIn.loc[tempIn.groupby(['year_month_day'])['Internal_Temp'].idxmin()].set_index('year_month_day')
tempInMax = tempIn.loc[tempIn.groupby(['year_month_day'])['Internal_Temp'].idxmax()].set_index('year_month_day')
tempIn = pd.concat([tempInMin,tempInMax] , axis=1, keys=('min','max'))
tempIn.columns = tempIn.columns.map('_'.join)



# In[308]:


tempOut = df[['CREATED','External_Temp','year_month_day']]
tempOutMin = tempOut.loc[tempOut.groupby(['year_month_day'])['External_Temp'].idxmin()].set_index('year_month_day')
tempOutMax = tempOut.loc[tempOut.groupby(['year_month_day'])['External_Temp'].idxmax()].set_index('year_month_day')
tempOut = pd.concat([tempOutMin,tempOutMax] , axis=1, keys=('min','max'))
tempOut.columns = tempOut.columns.map('_'.join)
print(tempOut)


# In[309]:


airPres = df[['CREATED','Pressure','year_month_day']]
airPresMin = airPres.loc[airPres.groupby(['year_month_day'])['Pressure'].idxmin()].set_index('year_month_day')
airPresMax = airPres.loc[airPres.groupby(['year_month_day'])['Pressure'].idxmax()].set_index('year_month_day')
airPres = pd.concat([airPresMin,airPresMax] , axis=1, keys=('min','max'))
airPres.columns = airPres.columns.map('_'.join)
print(airPres)


# In[310]:


hum = df[['CREATED','Humidity','year_month_day']]
humMin = hum.loc[hum.groupby(['year_month_day'])['Humidity'].idxmin()].set_index('year_month_day')
humMax = hum.loc[hum.groupby(['year_month_day'])['Humidity'].idxmax()].set_index('year_month_day')
hum = pd.concat([humMin,humMax] , axis=1, keys=('min','max'))
hum.columns = hum.columns.map('_'.join)
print(hum)


# In[311]:


avgdf = df.groupby('year_month_day')['Internal_Temp','External_Temp','Pressure','Humidity'].mean()
#avgdf = avgdf.rename(columns={'Internal_Temp':'Ave_Internal_Temp', 'GROUND_TEMPERATURE':'Ave_External_Temp', 'AIR_PRESSURE':'Ave_Pressure','Humidity':'Ave_Humidity'})
avgdf.columns = 'Average_' + avgdf.columns
avgdf.head()


# In[312]:


tempIn = tempIn.join(avgdf['Average_Internal_Temp'])
tempIn.head()
print(tempIn)

# In[313]:


tempIn.plot(y=['min_Internal_Temp','max_Internal_Temp','Average_Internal_Temp'], kind='bar')
#plt.show()


# In[314]:


tempOut = tempOut.join(avgdf['Average_External_Temp'])
print(tempOut)

# In[315]:


tempOut.plot(y=['min_External_Temp','max_External_Temp','Average_External_Temp'], kind='bar')
#plt.show()


# In[316]:


airPres = airPres.join(avgdf['Average_Pressure'])
print(airPres)

# In[317]:


airPres.plot(y=['min_Pressure','max_Pressure','Average_Pressure'], kind='bar')
#plt.show()


# In[318]:


hum = hum.join(avgdf['Average_Humidity'])
print(hum)

# In[319]:


hum.plot(y=['min_Humidity','max_Humidity','Average_Humidity'], kind='bar')
plt.show()


# In[ ]:




