# Libraries

import pandas as pd

# Preprocess

df = pd.read_csv(r'~/Projects/Solving_Delhi_pollution/data/Delhi_AQIBulletins.csv')

# Preprocess date feature
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

# Year
df['year'] = df['date'].apply(lambda x: int(str(x).split('-')[0]))

df.to_csv(r'data/preprocessed.csv')
