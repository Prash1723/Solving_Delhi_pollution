import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv(r'data/preprocessed.csv')

# Select features for model
df = data[['Index Value', 'Prominent Pollutant', 'year', 'month', 'SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']]

