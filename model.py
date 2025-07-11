import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import calendar

pd.options.mode.copy_on_write = True

data = pd.read_csv(r'data/preprocessed.csv')

# Preprocess month
month_list = list(calendar.month_abbr)
data['month'] = data['month'].apply(lambda x: month_list.index(x))

# Extract day
data['day'] = pd.to_datetime(data['date']).dt.day

# Select features for model
df = data[['Prominent Pollutant', 'year', 'month', 'day', 'SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']]

pol = pd.get_dummies(df['Prominent Pollutant'])

df.drop('Prominent Pollutant', axis=1, inplace=True)

X = pd.concat([df, pol], axis=1)

y = data['Index Value']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Create and train a linear regressor
lr = LinearRegression()
lr.fit(X_train, y_train)

# Make predictions
y_pred = lr.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

mae = mean_absolute_error(y_test, y_pred)

print("MSE : {0:.02f}".format(mse))

print("RMSE : {0:.02f}".format(rmse))

print("MAE : {0:.02f}".format(mae))

# Predictions for 2024
