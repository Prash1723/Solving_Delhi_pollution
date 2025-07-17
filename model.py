import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
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

# Preprocess year
year_dict = {
	2015: 1,
	2016: 2,
	2017: 3,
	2018: 4,
	2019: 5,
	2020: 6,
	2021: 7,
	2022: 8,
	2023: 9
}

data['year'] = data['year'].apply(lambda x: year_dict.get(x,x))

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

# Create and train a Lasso regressor
ls = Lasso()
ls.fit(X_train, y_train)

# Create and train a Lasso regressor
en = ElasticNet()
en.fit(X_train, y_train)

# Create and train a decision tree regressor
dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr.predict(X_test)
y_pred_ls = ls.predict(X_test)
y_pred_en = en.predict(X_test)
y_pred_dtr = dtr.predict(X_test)

# Evaluate the LR model
lr_mse = mean_squared_error(y_test, y_pred_lr)

lr_rmse = np.sqrt(lr_mse)

lr_mae = mean_absolute_error(y_test, y_pred_lr)

print('-'*20+'LinearRegression'+'-'*20)

print("LR MSE : {0:.02f}".format(lr_mse))

print("LR RMSE : {0:.02f}".format(lr_rmse))

print("LR MAE : {0:.02f}".format(lr_mae))

# Evaluate the Lasso model
ls_mse = mean_squared_error(y_test, y_pred_ls)

ls_rmse = np.sqrt(ls_mse)

ls_mae = mean_absolute_error(y_test, y_pred_ls)

print('-'*20+'LassoRegression'+'-'*20)

print("LS MSE : {0:.02f}".format(ls_mse))

print("LS RMSE : {0:.02f}".format(ls_rmse))

print("LS MAE : {0:.02f}".format(ls_mae))

# Evaluate the Lasso model
en_mse = mean_squared_error(y_test, y_pred_en)

en_rmse = np.sqrt(en_mse)

en_mae = mean_absolute_error(y_test, y_pred_en)

print('-'*20+'ElasticNet'+'-'*20)

print("EN MSE : {0:.02f}".format(en_mse))

print("EN RMSE : {0:.02f}".format(en_rmse))

print("EN MAE : {0:.02f}".format(en_mae))

# Evaluate the DTR model
dtr_mse = mean_squared_error(y_test, y_pred_dtr)

dtr_rmse = np.sqrt(dtr_mse)

dtr_mae = mean_absolute_error(y_test, y_pred_dtr)

print('-'*20+'DecisionTreeRegressor'+'-'*20)

print("DTR MSE : {0:.02f}".format(dtr_mse))

print("DTR RMSE : {0:.02f}".format(dtr_rmse))

print("DTR MAE : {0:.02f}".format(dtr_mae))