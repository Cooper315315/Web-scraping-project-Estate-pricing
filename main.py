import pandas as pd
import re
df = pd.read_csv('hk_property.csv')
df.drop(['Unnamed: 0','8'], axis = 1, inplace = True)
df.dropna(inplace = True)  # Remove first row of nan values

colnames = ['location', 'name', 'price', 'floor_area', 'floor', 'price/sq_ft', 'discount_rate', 'agency/self', 'date']
df.columns = colnames

df.date = pd.to_datetime(df.date)
df = df.set_index('date')

# Convert "string-numbers" into "integers".
df['discount_rate'] = df['discount_rate'].astype(int)
df['price'] = df['price'].apply(lambda x: x.replace(",", ""))
df['price'] = df['price'].astype(int)
df['floor_area'] = df['floor_area'].apply(lambda x: int(re.search('\w+', x).group()))
df['price/sq_ft'] = df['price/sq_ft'].apply(lambda x: int(x[:x.index("/")-1].replace(",", "")))

df.duplicated().sum()
df = df.drop_duplicates()
df