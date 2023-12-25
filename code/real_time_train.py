#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

secret_key = '6c5a66576979756e33334452684245'
start_urls = "http://swopenAPI.seoul.go.kr/api/subway"
url = f'{start_urls}/{secret_key}/xml/realtimeStationArrival/all'


# In[3]:


response = requests.get(url)


# In[4]:


soup = BeautifulSoup(response.text, "xml") # 실시간 도착 정보 받기


# In[5]:


soup


# In[6]:


station_2_id = pd.read_excel('station_information.xlsx', engine='openpyxl')
station_2_id.head()


# In[7]:


station_2_id = station_2_id[station_2_id['호선이름']=='2호선']
station_2_name = station_2_id['STATN_NM']
station_2_id = station_2_id['SUBWAY_ID']


# In[8]:


station_2_name


# In[9]:


import xml.etree.ElementTree as ET


# In[10]:


xml_data = soup.prettify()
root = ET.fromstring(xml_data)


# In[11]:


# 각 <row> 태그의 데이터를 리스트로 추출
rows = []
for row_elem in root.findall('row'):
    row_data = {}
    for child in row_elem:
        row_data[child.tag] = child.text
    rows.append(row_data)

# 리스트를 판다스 DataFrame으로 변환
df = pd.DataFrame(rows)
df = df.applymap(lambda x: x.replace('\n', '').strip())
df


# In[12]:


filtered_df = df[df['statnNm'].isin(station_2_name)]


# In[13]:


filtered_df


# In[14]:


# CSV 파일로 저장
filtered_df.to_csv('real_time_train_data.csv', index=False)


# In[ ]:




