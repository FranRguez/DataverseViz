
# coding: utf-8

# #

# In[ ]:





# # FIGURA: METRICS FILES/DOWNLOADS VISUALIZATION

# In[190]:


import datetime
import calendar
import requests
import json

rangeofmonths=36
prueba = requests.Session()
files=[]
downloads=[]
month=[]


def change_months(datetoday, months):
     month = datetoday.month - 1 + months
     year = datetoday.year + month // 12
     month = month % 12 + 1
     day = min(datetoday.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)


for i in range (1, rangeofmonths+1):
    # Get the month
    month.append(str(change_months(datetoday,-i).strftime("%m/%Y")))
    
    # Get number of files uploaded this month
    url="https://dataverse.harvard.edu/api/info/metrics/files/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    files.append(data['data']['count'])
    
    # Get number of downloads this month
    url="https://dataverse.harvard.edu/api/info/metrics/downloads/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    downloads.append(data['data']['count'])

months=pd.DataFrame(month, columns=['Month'])
files_df=pd.DataFrame(files, columns=['FilesUploaded'])
downloads_df=pd.DataFrame(downloads, columns=['DownloadsUploaded'])
downloadsperfile_df=pd.DataFrame(downloads_df['DownloadsUploaded']/files_df['FilesUploaded'],columns=['DownloadsPerFile'])



draft=pd.merge(months, files_df,left_index=True, right_index=True)
draft2=pd.merge(draft,downloads_df, left_index=True,right_index=True)
final=pd.merge(draft2, downloadsperfile_df, left_index=True,right_index=True)

print(final)


# In[187]:


final.to_csv('filesdownloads.csv', sep=';', encoding='utf_16')


# # 1 SHOW NAME AND TYPE OF UPLOADS AT HARVARD DATAVERSE

# In[15]:


#!/usr/bin/env python
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
base = 'https://dataverse.harvard.edu'
rows = 10
start = 0
page = 1
condition = True # emulate do-while
prueba = requests.Session()
retry = Retry(connect=3, backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry)
prueba.mount('http://', adapter)
prueba.mount('https://', adapter)


while (condition):
    url = base + '/api/search?q=*&per_page=10' + "&start=" + str(start)
    data = json.loads(prueba.get(url).text)
    total = data['data']['total_count']
    print("=== Page", page, "===")
    print("start:", start, " total:", total)
    for i in data['data']['items']:
        print("- ", i['name'], "(" + i['type'] + ")")
    start = start + rows
    page += 1
    condition = start < total/5


# # FIGURAS 1 y 2: TOTALES # 2 1+ DATABASE CREATION

# In[ ]:


#!/usr/bin/env python
import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

base = 'https://dataverse.harvard.edu'
rows = 1000
start = 0
page = 1
condition = True # emulate do-while
prueba = requests.Session()
retry = Retry(connect=3, backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry)
prueba.mount('http://', adapter)
prueba.mount('https://', adapter)
scraping_types=pd.DataFrame(columns=['Type'])
scraping_names=pd.DataFrame(columns=['Name'])
scraping_publication=pd.DataFrame(columns=['PublicationDate'])



while (condition):
    url = base + '/api/search?q=*&per_page=1000&show_facets=true' + "&start=" + str(start)
    data = json.loads(prueba.get(url).text)
    total = data['data']['total_count']
    print("=== Page", page, "===")
    print("start:", start, " total:", total)
    for i in data['data']['items']:
        print("- ", i['name'], "(" + i['type'] + ")")
        scraping_types=scraping_types.append(pd.DataFrame([i['type']], columns=['Type']))
        scraping_names=scraping_names.append(pd.DataFrame([i['name']], columns=['Name']))
        scraping_publication=scraping_publication.append(pd.DataFrame([i['published_at']], columns=['PublicationDate']))

    start = start + rows
    page += 1
    condition = start < total/5
                    


# # MERGE DATAFRAMES

# In[ ]:


scraping1=scraping_names.reset_index()
scraping2=scraping_types.reset_index()
scraping3=scraping_publication.reset_index()

casifinal=pd.merge(scraping1, scraping2, left_index=True, right_index=True)
casifinal=pd.merge(casifinal, scraping3, left_index=True, right_index=True)
casifinal=casifinal.drop(['index_y', 'index_x', 'index'], axis=1)
print(casifinal)


# In[20]:


casifinal.to_csv('index.csv', sep=';', encoding='utf_16')


# In[72]:


import datetime
import calendar
import requests
import json
import pandas as pd

rangeofmonths=36
prueba = requests.Session()
files=[]
downloads=[]
month=[]
datetoday=datetime.datetime.today()


def change_months(datetoday, months):
     month = datetoday.month - 1 + months
     year = datetoday.year + month // 12
     month = month % 12 + 1
     day = min(datetoday.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

print(change_months(datetoday,-i))
    
    
for i in range (1, rangeofmonths+1):
    # Get the month
    month.append(str(change_months(datetoday,-i).strftime("%m/%Y")))
    
    # Get number of files uploaded this month
    url="https://dataverse.harvard.edu/api/info/metrics/files/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    files.append(data['data']['count'])
    
    # Get number of downloads this month
    url="https://dataverse.harvard.edu/api/info/metrics/downloads/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    downloads.append(data['data']['count'])

months=pd.DataFrame(month, columns=['Month'])
files_df=pd.DataFrame(files, columns=['FilesUploaded'])
downloads_df=pd.DataFrame(downloads, columns=['DownloadsUploaded'])
downloadsperfile_df=pd.DataFrame(downloads_df['DownloadsUploaded']/files_df['FilesUploaded'],columns=['DownloadsPerFile'])



draft=pd.merge(months, files_df,left_index=True, right_index=True)
draft2=pd.merge(draft,downloads_df, left_index=True,right_index=True)
final=pd.merge(draft2, downloadsperfile_df, left_index=True,right_index=True)

print(final)


# In[109]:


import datetime
import calendar
import requests
import json
import pandas as pd

prueba = requests.Session()
files=[]
downloads=[]
dataverses=[]
datasets=[]
month=[]
datetoday=datetime.datetime.today()


def change_months(datetoday, months):
     month = datetoday.month - 1 + months
     year = datetoday.year + month // 12
     month = month % 12 + 1
     day = min(datetoday.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

from datetime import datetime
from dateutil import relativedelta
date1 = datetime.strptime('2007-11-01 12:00:00', '%Y-%m-%d %H:%M:%S')
date2 = datetime.strptime(datetoday.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
r = relativedelta.relativedelta(date2, date1)
monthsfromdataversecreation=(r.years)*12+r.months
print(monthsfromdataversecreation)


import datetime
for i in range (1, monthsfromdataversecreation+1):
    # Get the today's month
    month.append(str(change_months(datetoday,-i).strftime("%m/%Y")))
    
    # Get evolution of number of files uploaded since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/files/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    files.append(data['data']['count'])
    
    # Get evolution of number of downloads since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/downloads/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    downloads.append(data['data']['count'])
    
    # Get evolution of number of dataverses since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/dataverses/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    dataverses.append(data['data']['count'])
    
    
    # Get evolution of number of datasets since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/datasets/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    datasets.append(data['data']['count'])
    
# CREATING FIRST DATABASE: RELATIONSHIP BETWEEN FILES AND DOWNLOADS.
months=pd.DataFrame(month, columns=['Month'])
files_df=pd.DataFrame(files, columns=['FilesUploaded'])
downloads_df=pd.DataFrame(downloads, columns=['DownloadsUploaded'])
downloadsperfile_df=pd.DataFrame(downloads_df['DownloadsUploaded']/files_df['FilesUploaded'],columns=['DownloadsPerFile'])

draft=pd.merge(months, files_df,left_index=True, right_index=True)
draft2=pd.merge(draft,downloads_df, left_index=True,right_index=True)
final=pd.merge(draft2, downloadsperfile_df, left_index=True,right_index=True)
print(final)

# CREATING SECOND DATABASE: RELATIONSHIP BETWEEN NUMBER OF DATAVERSEs, DATASETS AND FILES.
dataverses_df=pd.DataFrame(dataverses, columns=['NumberOfDataverse'])
datasets_df=pd.DataFrame(datasets, columns=['NumberOfDatasets'])
draft_seconddatabase=pd.merge(draft, dataverses_df, left_index=True, right_index=True)
final_second=pd.merge(draft_seconddatabase, datasets_df, left_index=True, right_index=True)
print(final_second)


# In[110]:


# EXPORT TO CSV
final.to_csv('datafiles_downloads.csv', sep=';', encoding='utf_16')
final_second.to_csv('evolution.csv', sep=';', encoding='utf_16')


# # SAME BUT WITHIN ONE COLUMN

# In[188]:


import datetime
import calendar
import requests
import json
import pandas as pd

prueba = requests.Session()
files=[]
downloads=[]
dataverses=[]
datasets=[]
month=[]
datetoday=datetime.datetime.today()


def change_months(datetoday, months):
     month = datetoday.month - 1 + months
     year = datetoday.year + month // 12
     month = month % 12 + 1
     day = min(datetoday.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

from datetime import datetime
from dateutil import relativedelta
date1 = datetime.strptime('2007-11-01 12:00:00', '%Y-%m-%d %H:%M:%S')
date2 = datetime.strptime(datetoday.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
r = relativedelta.relativedelta(date2, date1)
monthsfromdataversecreation=(r.years)*12+r.months
print(monthsfromdataversecreation)

import datetime
for i in range (1, monthsfromdataversecreation+1):
    # Get the today's month
    month.append(str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m")))
    
    # Get evolution of number of files uploaded since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/files/toMonth/"+str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    files.append(data['data']['count'])
    
    # Get evolution of number of downloads since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/downloads/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    downloads.append(data['data']['count'])
    
    # Get evolution of number of dataverses since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/dataverses/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    dataverses.append(data['data']['count'])
    
    
    # Get evolution of number of datasets since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/datasets/toMonth/"+str(change_months(datetoday,-i).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    datasets.append(data['data']['count'])
    
# CREATING FIRST DATABASE: RELATIONSHIP BETWEEN FILES AND DOWNLOADS.
months=pd.DataFrame(month, columns=['Month'])
files_df=pd.DataFrame(files, columns=['UploadsNumber'])
downloads_df=pd.DataFrame(downloads, columns=['UploadsNumber'])
downloadsperfile_df=pd.DataFrame(downloads_df['UploadsNumber']/files_df['UploadsNumber'],columns=['UploadsNumber'])

draft=pd.merge(months, files_df,left_index=True, right_index=True)
draft2=pd.merge(draft,downloads_df, left_index=True,right_index=True)
final=pd.merge(draft2, downloadsperfile_df, left_index=True,right_index=True)
print(final)

# CREATING SECOND DATABASE: RELATIONSHIP BETWEEN NUMBER OF DATAVERSEs, DATASETS AND FILES. First, I add the column origin's name.
files_df['Type']="Files"
files_df_final=pd.merge(months,files_df, left_index=True,right_index=True)

dataverses_df=pd.DataFrame(dataverses, columns=['UploadsNumber'])
dataverses_df['Type']="Dataverse"
dataverses_df_final=pd.merge(months,dataverses_df, left_index=True,right_index=True)

datasets_df=pd.DataFrame(datasets, columns=['UploadsNumber'])
datasets_df['Type']="Datasets"
datasets_df_final=pd.merge(months,datasets_df, left_index=True,right_index=True)


cumulativetotals=pd.concat([downloads_df_final, dataverses_df_final, datasets_df_final])
print(cumulativetotals)


# ## SAME BUT WITHIN ONE COLUMN AND ONLY ADDED VALUES

# In[184]:


import datetime
import calendar
import requests
import json
import pandas as pd

prueba = requests.Session()
files=[]
downloads=[]
dataverses=[]
datasets=[]
month=[]
datetoday=datetime.datetime.today()


def change_months(datetoday, months):
     month = datetoday.month - 1 + months
     year = datetoday.year + month // 12
     month = month % 12 + 1
     day = min(datetoday.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

from datetime import datetime
from dateutil import relativedelta
date1 = datetime.strptime('2007-11-01 12:00:00', '%Y-%m-%d %H:%M:%S')
date2 = datetime.strptime(datetoday.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
r = relativedelta.relativedelta(date2, date1)
monthsfromdataversecreation=(r.years)*12+r.months
print(monthsfromdataversecreation)


import datetime
for i in range (1, monthsfromdataversecreation+1):
    # Get the today's month
    month.append(str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m")))
    # Get evolution of number of files uploaded since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/files/toMonth/"+str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    if i == 1:
        files.append(0)
        keepvalue=data['data']['count']
    if i > 1:
        files.append(data['data']['count']-keepvalue)
        keepvalue=data['data']['count']
    
    # Get evolution of number of downloads since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/downloads/toMonth/"+str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    if i == 1:
        downloads.append(0)
        keepvalue2=data['data']['count']
    if i > 1:
        downloads.append(data['data']['count']-keepvalue2)
        keepvalue2=data['data']['count']
    
    # Get evolution of number of dataverses since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/dataverses/toMonth/"+str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    if i == 1:
        dataverses.append(0)
        keepvalue3=data['data']['count']
    if i > 1:

        dataverses.append(data['data']['count']-keepvalue3)
        keepvalue3=[]
        keepvalue3=data['data']['count']

    # Get evolution of number of datasets since the beginning of the (data)universe
    url="https://dataverse.harvard.edu/api/info/metrics/datasets/toMonth/"+str(change_months(datetoday,-monthsfromdataversecreation+i-1).strftime("%Y-%m"))
    data = json.loads(prueba.get(url).text)
    if i == 1:
        datasets.append(0)
        keepvalue4=data['data']['count']
    if i > 1:
        datasets.append(data['data']['count']-keepvalue4)
        keepvalue4=data['data']['count']
    
# CREATING FIRST DATABASE: RELATIONSHIP BETWEEN FILES AND DOWNLOADS.
months=pd.DataFrame(month, columns=['Month'])
files_df=pd.DataFrame(files, columns=['UploadsNumber'])
downloads_df=pd.DataFrame(downloads, columns=['UploadsNumber'])
downloadsperfile_df=pd.DataFrame(downloads_df['UploadsNumber']/files_df['UploadsNumber'],columns=['UploadsNumber'])

draft=pd.merge(months, files_df,left_index=True, right_index=True)
draft2=pd.merge(draft,downloads_df, left_index=True,right_index=True)
final=pd.merge(draft2, downloadsperfile_df, left_index=True,right_index=True)
print(final)

# CREATING SECOND DATABASE: RELATIONSHIP BETWEEN NUMBER OF DATAVERSEs, DATASETS AND FILES. First, I add the column origin's name.
files_df['Type']="Files"
files_df_final=pd.merge(months,files_df, left_index=True,right_index=True)

dataverses_df=pd.DataFrame(dataverses, columns=['UploadsNumber'])
dataverses_df['Type']="Dataverse"
dataverses_df_final=pd.merge(months,dataverses_df, left_index=True,right_index=True)

datasets_df=pd.DataFrame(datasets, columns=['UploadsNumber'])
datasets_df['Type']="Datasets"
datasets_df_final=pd.merge(months,datasets_df, left_index=True,right_index=True)


addedtotals=pd.concat([files_df_final, dataverses_df_final, datasets_df_final])
print(addedtotals)


# In[191]:


addedtotals.to_csv('added.csv', sep=";")


# In[192]:


addedtotals['Operation']="New added"
cumulativetotals['Operation']="Cumulative"


# In[193]:


final=pd.concat([addedtotals,cumulativetotals])
print(final)
final.to_csv('final.csv', sep=";")

