import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv(r'data/preprocessed.csv')

# Select features for model
X = data[['Prominent Pollutant', 'year', 'month', 'SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']]

y = data['Index Value']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Create and train a linear regressor
lr = LinearRegression()
lr.fit(X_train, y_train)

# Make predictions
y_pred = lr.predict(X_test)

# Evaluate the model
