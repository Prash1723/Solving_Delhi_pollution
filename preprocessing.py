# Libraries
import pandas as pd

# Load data
df = pd.read_csv(r'data/Delhi_AQIBulletins.csv')

# Preprocess date feature
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

# Year
df['year'] = df['date'].apply(lambda x: int(str(x).split('-')[0]))

# Air Quality
df['Air Quality'] = df['Air Quality'].apply(lambda s: 'Very Poor' if 'Very poor' in s else s)

# Create list of unique pollutants
values = []
combo_pollutants = df['Prominent Pollutant'].apply(lambda x: x.split(', ')).tolist()		# Combination of pollutants

for i in combo_pollutants:
	values.extend(i)

pollutants = list(set(values))																# Unique pollutants

# Create sparse data for individual pollutants
for i in pollutants:
	df[i] = df['Prominent Pollutant'].apply(lambda s: 1 if i in s else 0)

# Save it to CSV file
df.to_csv('data/preprocessed.csv', index=False)