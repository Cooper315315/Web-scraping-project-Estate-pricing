# Web-scraping-project-Estate-pricing

<h3>Goal: Find insights and actions plans from estate pricing data</h3>

<!-- ################################################################################################ -->

<br/>
<h3>Data Collection: Web Scraping</h3>
<img width="800" alt="DF" src="https://user-images.githubusercontent.com/80112729/119645828-0a567a00-be51-11eb-8754-bd2097b0be94.png">
<br/>

Step 1: Import necessary libraries 
```
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import regex as re
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import itertools
```
Step 2: Scrape the website
```
year = [str(y) for y in range(2002,2022)]
month = list(range(1,13))
month = [str(m).zfill(2) for m in month]
calendar = list(itertools.product(year, month))[:-9]
new_table = pd.DataFrame(columns=range(9),index=[0])
URL_generic = 'https://www.housingauthority.gov.hk/en/home-ownership/hos-secondary-market/transaction-records/transaction-records-search-detail-by-month.html?catId=1&'
driver = webdriver.Chrome('./chromedriver')
for c in calendar:
    URL = URL_generic + 'para0='+c[0]+'&para1='+c[1]
    driver.get(URL)
    subhtml = driver.page_source
    soup = BeautifulSoup(subhtml, "html.parser")
    table = soup.find_all('table')
    for t in table:
        row=[]
        tr = t.tbody.find_all('tr')
        for i in tr:
            element = []
            for j in i.find_all('td'):
                element.append(j.get_text())
            row.append(element)
        for n in range(len(row)):
            sub_table = pd.DataFrame(row[n]).T
            sub_table['8']=c[0]+'-'+c[1]
            new_table = new_table.append(sub_table)
new_table.to_csv('hk_property.csv')
```

Step 1: Request and parse website as HTML using Selenium and BS4

Step 2: Find all "table" "tr" and "td" elements and extract contents via get_text()

Step 3: Loop through the above process through all the months and years from 2002 (240 pages in total)


<!-- ################################################################################################ -->

<h3>Data Preprocessing: Data Cleaning</h3>

<br/>
<h3>Original DataFrame:</h3>
<img width="500" alt="DF" src="https://user-images.githubusercontent.com/80112729/119641257-0bd17380-be4c-11eb-983f-3c917644892e.png">
<br/>

```
Step 1: Remove unnecessary columns

Step 2: Checking for null values

Step 3: Rename columns

Step 4: Convert date column as datetime type and set it as index

Step 5: Convert string numbers into numerical values

Step 6: Check and remove duplicate values
```

<br/>
<h3>Finalised DataFrame:</h3>
<img width="800" alt="DF" src="https://user-images.githubusercontent.com/80112729/119642065-eb55e900-be4c-11eb-9b87-4e99a3b3456a.png">
<br/>

```
Note 1: 1 sq m = 10.764 sq ft.

Note 2: "H": 27/F or above; "M": 14/F to 26/F; "L": 13/F or below.
```

<!-- ################################################################################################ -->

<h3>The Most Popular Property Types:</h3>

<br/>
<img width="1000" alt="Propertytype" src="https://user-images.githubusercontent.com/80112729/119647006-5ce46600-be52-11eb-84b4-36b4bb67c04b.png">
From 2002 to 2021, most transaction sales were made in Tseung Kwan O, Tin Shui Wai, Tuen Mun and Ma On Shan. And the floor types include all three, which are higher, middle and lower floor.
<br/>



<h3>Price per sq ft over time:</h3>

<br/>
<img width="1000" alt="Priceovertime" src="https://user-images.githubusercontent.com/80112729/119647808-4a1e6100-be53-11eb-99b4-956c0fa13629.png">
For Tseung Kwan O, Tin Shui Wai, Tuen Mun and Ma On Shan. the transaction price per sq ft increases with time. But the increment starts to flatten around 2019.
<br/>

