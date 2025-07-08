import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import calendar

data = pd.read_csv(r'data/preprocessed.csv')

# Preprocess month
month_list = list(calendar.month_abbr)
data['month'] = data['month'].apply(lambda x: month_list.index(x))

# Select features for model
X = data[['Prominent Pollutant', 'year', 'month', 'SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']]

pol = pd.get_dummies(X['Prominent Pollutant'])

y = data['Index Value']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Create and train a linear regressor
lr = LinearRegression()
lr.fit(X_train, y_train)

# Make predictions
y_pred = lr.predict(X_test)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("RMSE : {%f}", rmse)