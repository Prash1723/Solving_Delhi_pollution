# Libraries
import pandas as pd
import calendar

# Load data
df = pd.read_csv(r'data/Delhi_AQIBulletins.csv')

# Preprocess date feature
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

# Year
df['year'] = df['date'].apply(lambda x: int(str(x).split('-')[0]))

# Air Quality
df['Air Quality'] = df['Air Quality'].apply(lambda s: 'Very Poor' if 'Very poor' in s else s)

# Season
season_dict = {
	'Jan': "winter",
	'Feb': "winter",
	'Mar': "summer",
	'Apr': "summer",
	'May': "summer",
	'Jun': "summer",
	'Jul': "monsoon",
	'Aug': "monsoon",
	'Sep': "monsoon",
	'Oct': "monsoon",
	'Nov': "winter",
	'Dec': "winter"
}

df['month'] = df['date'].dt.month

df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

df['season'] = df['month'].apply(lambda x : season_dict.get(str(x), x))

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