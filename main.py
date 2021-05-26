from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import regex as re
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

#Scraping HOS Data
import itertools
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

#Scraping HK Property Data
URL = 'https://www.property.hk/eng/price_indices.php'
driver = webdriver.Chrome('./chromedriver')
driver.get(URL)
subhtml = driver.page_source
soup = BeautifulSoup(subhtml, "html.parser")
table = soup.find_all('table')
rows=[]

for i in soup.find_all('table'):
    element = []
    for j in i.find_all(class_='col-xs-12',id='tran12'):
        element.append(j.get_text())
    rows.append(element)
    content = rows[1][0].split('\n')

title = content[2:7]
data = content[8:]
data1 = content[8:data.index('Month')+8]
data2 = content[data.index('Month')+6+8:]
data = data1+data2
chunks = [y[:-2] for y in [data[x:x+7] for x in range(0, len(data)-350, 7)]]

hsp = pd.DataFrame(columns=range(5),index=[])
for c in chunks:
    row = pd.DataFrame(c).T
    hsp = hsp.append(row)
hsp.columns=title

#Process HOS Data
df = pd.read_csv('hk_property.csv')
df.drop(['Unnamed: 0','8'], axis = 1, inplace = True)
df.dropna(inplace = True)  # Remove first row of nan values

colnames = ['location', 'name', 'price', 'floor_area', 'floor', 'price/sq_ft', 'discount_rate', 'agency/self', 'date']
df.columns = colnames

df.date = pd.to_datetime(df.date)
df = df.set_index('date')

#Convert "string-numbers" into "integers".
df['discount_rate'] = df['discount_rate'].astype(int)
df['price'] = df['price'].apply(lambda x: x.replace(",", ""))
df['price'] = df['price'].astype(int)
df['floor_area'] = df['floor_area'].apply(lambda x: int(re.search('\w+', x).group()))
df['price/sq_ft'] = df['price/sq_ft'].apply(lambda x: int(x[:x.index("/")-1].replace(",", "")))

df.duplicated().sum()
df = df.drop_duplicates()

#Process HK Property Data
df_hist['Month']=df_hist['date'].apply(lambda x: x.strftime('%b-%y'))
mkt = df_hist.merge(hsp,on='Month')
mkt = mkt.iloc[:-1,:]
mkt['Domestic']=mkt['Domestic'].astype(float)
mkt['Offices']=mkt['Offices'].astype(float)
mkt['Retail']=mkt['Retail'].astype(float)
mkt['hso_norm']=(mkt.price/mkt.price.iloc[0])*100
mkt['resi_norm']=(mkt.Domestic/mkt.Domestic.iloc[0])*100
mkt['office_norm']=(mkt.Offices/mkt.Offices.iloc[0])*100
mkt['retail_norm']=(mkt.Retail/mkt.Retail.iloc[0])*100

#Visualization

#y-axis formatter
from matplotlib.ticker import FuncFormatter
def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0fM' % (x * 1e-6)

formatter = FuncFormatter(millions)

#Historical price & transaction

df_hist = df.groupby('date')['price'].mean().to_frame().reset_index()
df_volume = df.copy()
df_volume['volume']=1
df_hist['volume'] = df_volume.groupby('date')['volume'].sum().to_list()

fig = plt.figure(figsize=(20,8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot('Month', 'hso_norm', data=mkt,color='Navy')
ax1.plot('Month', 'resi_norm', data=mkt,color='Dodgerblue')
ax1.plot('Month', 'office_norm', data=mkt,color='Firebrick')
ax1.plot('Month', 'retail_norm', data=mkt,color='Lightsalmon')
start, end = ax1.get_xlim()
ax1.xaxis.set_ticks(np.arange(start, end, 20))
legend=['HOS Housing','Private Residential','Offices','Retail']
ax1.legend(legend,fontsize=12)
ax1.set_title('Hong Kong Property Price Trend - HOS vs Private Market',fontsize=14)
ax1.set_xlabel('Date')
ax1.set_ylabel('Normalized price')

sns.lineplot(data=df_hist,x='date',y='volume',ax=ax2)
ax2.set_title('Monthly HOS Transactions',fontsize=14)
ax2.set_xlabel('Date')
ax2.set_ylabel('Transaction Volumes')
ax2.axhline(df_hist.volume.mean(),color='Red',linestyle='--')
plt.tight_layout()
plt.show()

fig.savefig('property price & volume.png')

#Transaction / discount rate data by area

df_area = df.groupby('location').mean().reset_index()
df_area['volume']=df_volume.groupby('location')['volume'].sum().to_list()

fig,ax = plt.subplots(figsize=(18,8))
sns.scatterplot(ax=ax, data=df_area, x="discount_rate", y="price", hue="location",legend=False,
                size='volume',sizes=(50,2000),palette='coolwarm')
ax.yaxis.set_major_formatter(formatter)


def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

label_point(df_area.discount_rate, df_area.price, df_area.location, plt.gca()) 

ax.set_title('Transaction price vs discount rate per area',fontsize=14)
ax.set_xlabel('Discount Rate (%)')
ax.set_ylabel('Average Transaction Price (HK$)')
plt.show()
plt.tight_layout()

fig.savefig('price vs discount rate.png',bbox_inches='tight')


# Visualissation (Cooper)
df2 = df.copy()
df2


fig,ax = plt.subplots(figsize=(20,10))
df2.groupby('location')['floor'].value_counts().sort_values(ascending = False).plot.bar()
ax.set_title('location & floor vs value counts',fontsize=14)
ax.set_xlabel('location & floor')
ax.set_ylabel('Value counts')
plt.show()
plt.tight_layout()


df2.groupby('location')['floor'].value_counts().sort_values(ascending=False).head(10)


# TSW
TSW = df2[df['location'] == 'Tin Shui Wai']
# Tseung Kwan O
TKO = df2[df['location'] == 'Tseung Kwan O']
# Tuen Mun
TM = df2[df['location'] == 'Tuen Mun']
# Ma On Shan
MOS = df2[df['location'] == 'Ma On Shan']


plt.figure(figsize=(20,10))
# Tin shui wai
plt.subplot(2,2,1) # 1st row, with 4 columns and position 1 on the output(The left). 
sns.lineplot(data = TSW, x = TSW.index, y = TSW['price/sq_ft']).set(title='Tin shui wai')
# Tseung Kwan O
plt.subplot(2,2,2) 
sns.lineplot(data = TKO, x = TKO.index, y = TKO['price/sq_ft']).set(title='Tseung Kwan O')
#Tuen Mun
plt.subplot(2,2,3) 
sns.lineplot(data = TM, x = TM.index, y = TM['price/sq_ft']).set(title='Tuen Mun')
# Ma On Shan
plt.subplot(2,2,4)
sns.lineplot(data = MOS, x = MOS.index, y = MOS['price/sq_ft']).set(title='Ma On Shan')


plt.figure(figsize=(30,20))
# Tin shui wai
plt.subplot(2,2,1) # 1st row, with 4 columns and position 1 on the output(The left). 
sns.lineplot(data = TSW, x = TSW.index, y = TSW['price/sq_ft'], color='red', label="Tin shui wai")
# Tseung Kwan O
sns.lineplot(data = TKO, x = TKO.index, y = TKO['price/sq_ft'], color='blue', label="Tseung Kwan O")
#Tuen Mun
sns.lineplot(data = TM, x = TM.index, y = TM['price/sq_ft'], color='green', label="Tuen Mun")
# Ma On Shan
sns.lineplot(data = MOS, x = MOS.index, y = MOS['price/sq_ft'], color='yellow', label="Ma On Shan").set(title='Date vs Price Per Sq Ft')


# Import dataset
df = pd.read_csv('hk_property.csv')
df.columns = ['Location', 'Court/Estate Name', 'Transaction Price (HK$)',
       'Saleable Floor Area (sq ft/sq m)', 'Floor',
       'Transaction Price per sq ft/sq m (Saleable Floor Area) (HK$)',
       'Discount Rate (%)', 'Agency (A)/Self-negotiation (S)']

# Remove unnecessary columns
df.drop(['Unnamed: 0','8'], axis = 1, inplace = True)

# df.isnull().sum() # Check for nan vaues
df.dropna(inplace = True)  # Remove first row of nan values

# #Rename columns
colnames = ['Location', 'Court/Estate Name', 'Transaction Price (HK$)', 'Saleable Floor Area (sq ft/sq m)', 'Floor', 'Transaction Price per sq ft/sq m (Saleable Floor Area) (HK$)', 'Discount Rate (%)', 'Agency (A)/Self-negotiation (S)', 'Date']  
df.columns = colnames

# Convert datetime:
df.Date = pd.to_datetime(df.Date)

# Set location as index
df = df.set_index('Date')

# Convert "string-numbers" into "integers".
df['Discount Rate (%)'] = df['Discount Rate (%)'].astype(int)
df['Transaction Price (HK$)'] = df['Transaction Price (HK$)'].apply(lambda x: x.replace(",", ""))
df['Transaction Price (HK$)'] = df['Transaction Price (HK$)'].astype(int)
df['Saleable Floor Area (sq ft/sq m)'] = df['Saleable Floor Area (sq ft/sq m)'].apply(lambda x: int(re.search('\w+', x).group()))
df['Transaction Price per sq ft/sq m (Saleable Floor Area) (HK$)'] = df['Transaction Price per sq ft/sq m (Saleable Floor Area) (HK$)'].apply(lambda x: int(x[:x.index("/")-1].replace(",", "")))

with sns.axes_style("white"):
    g = sns.FacetGrid(df, row="Location", col="Floor", margin_titles=True, height=2.5)
g.map(sns.scatterplot,"Saleable Floor Area (sq ft/sq m)", "Transaction Price (HK$)", color="#334488")
g.set_axis_labels("Area", "price")
g.set(xticks=[10, 30, 50], yticks=[2, 6, 10])
g.fig.subplots_adjust(wspace=.02, hspace=.02)


with sns.axes_style("white"):
    g = sns.FacetGrid(df, row="Location", col="Floor", margin_titles=True, height=2.5)
g.map(sns.scatterplot,"Saleable Floor Area (sq ft/sq m)", "normalized_price", color="#334488")
g.set_axis_labels("Area", "price")
g.set(xticks=[10, 30, 50], yticks=[2, 6, 10])
g.fig.subplots_adjust(wspace=.02, hspace=.02)


df.plot.scatter(x='Transaction Price (HK$)',y = 'Saleable Floor Area (sq ft/sq m)',s=0.5)

df.plot.scatter(x='Date',y = 'Transaction Price (HK$)',s=0.25)

#prototype of house price estimator
#input: 1. Location (or court/estate)
#       2. Saleable Floor Area
#       3. Floor
#output: 1. estimated price
#        2. closest case

#for each location and each floor

df.reset_index(inplace=True)
df

df[df['Location']=='Diamond Hill'].plot.scatter(x='Date',y = 'Transaction Price (HK$)',s=0.25)

# estimate the inflation rate by month #Assume inflation rate is unrelated to quality of house and only related to the time
# Assume distribution of house price is similar (or in the same family) with respect to time.
df[(df['Date'] == '2002-01-01') & (df.Location == 'Diamond Hill')]['Transaction Price (HK$)']


inflation_series = df.groupby('Date')['Transaction Price (HK$)'].mean()
now_rate = inflation_series[-1]

inflation_series = inflation_series.apply(lambda x: now_rate/x)
inflation_series

inflation_series['2021-03-01']

df_dateindex = df.set_index('Date')
df_dateindex

df['inflation'] = df['Date'].apply(lambda x: inflation_series[x])
df

#normalized to last month price, assume no inflation rate between last and this month: current price!
df['normalized_price'] = df['Transaction Price (HK$)']*df['inflation']

df.plot.scatter(x='Date',y='normalized_price',s=0.5)

df[df['Location']=='Diamond Hill'].plot.scatter(x='Date',y='Transaction Price (HK$)')

df[df['Location']=='Diamond Hill'].plot.scatter(x='Date',y='normalized_price')

df[df['Location']=='Diamond Hill'].plot.scatter(x='Saleable Floor Area (sq ft/sq m)',y='normalized_price')

def find_nearest_point(Location, Floor, area, df):
    if (Location not in df['Location'].unique()) or (Floor not in df['Floor'].unique()):
        print('Wrong location or floor input.')
        return None

    sub_df = df[(df["Location"] == Location) & (df['Floor'] == Floor)]
    if sub_df.shape[0]:
        cases = sub_df[(sub_df['Saleable Floor Area (sq ft/sq m)']<area+15) & (sub_df['Saleable Floor Area (sq ft/sq m)']>area-15)]
        if not cases.shape[0]:
            cases = sub_df
    else:
        cases = df[df["Location"] == Location]
    price = cases['normalized_price'].sum()/cases['Saleable Floor Area (sq ft/sq m)'].sum() * area
    return price,cases

testing_df = df[df['Date']< '2021-03-01']

validation_df = df[df['Date'] == '2021-03-01']

validation_df['Date'].shape
df.info()

prediction_list = [find_nearest_point(location, floor, area, testing_df)[0] for location, floor, area in zip(validation_df['Location'], validation_df['Floor'], validation_df['Saleable Floor Area (sq ft/sq m)'])]

#percentage AE
AE_pct = [ abs(predict-true)/true for predict, true in zip(prediction_list, validation_df['Transaction Price (HK$)'].to_list())]

#print
df_error = pd.DataFrame({'error':MAE_pct})
df_error.plot.kde()

#MAE
df_error.sum()/df_error.shape[0]
#error=    0.1211

#test if it tends to overshoot or undershoot
E_pct = [ (predict-true)/true for predict, true in zip(prediction_list, validation_df['Transaction Price (HK$)'].to_list())]
pn = [1 if i >0 else -1 for i in E_pct]
sum(pn)

find_nearest_point('Tsuen Wan', 'M', 430, df)
sub_df = df[(df['Floor'] == 'M') & (df['Location'] == 'Tsuen Wan')]
sub_df['Transaction Price (HK$)'].sum()/sub_df['Saleable Floor Area (sq ft/sq m)'].sum()*438
sub_df
df_dateindex
