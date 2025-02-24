import pandas as pd
from datetime import datetime

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, RangeSlider
from bokeh.models import Tabs, TabPanel
from bokeh.plotting import figure

df = pd.read_csv(r'~/Desktop/scripting/python/projects/AQI Delhi/data/Delhi_AQIBulletins.csv')

# Preprocess date feature
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

# Year
df['year'] = df['date'].apply(lambda x: int(str(x).split('-')[0]))

print(df['year'])

# Source
source = ColumnDataSource(df)

# Create widgets
date_range = RangeSlider(
	title="Select range of year",
	value=(2015, 2023),
	start=2015,
	end=2023,
	step=1
	)

pollutant_select = Select(
	title="Select Pollutant",
	value="All",
	options=["All"] + list(set(df['Prominent Pollutant']))
	)

# Figure
p = figure(
	x_axis_type="datetime",
	title="AQI trend line",
	height=400,
	width=700
	)

p.line("date", "Index Value", source=source, line_width=2)
p.scatter("date", "Index Value", source=source, size=3, color="red")
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "AQI Value"

# App

def update_chart():
	slider_value = date_range.value
	slider_low_range = slider_value[0]
	slider_high_range = slider_value[1]
	selected_pollutant = pollutant_select.value

	filtered_data = df.query("year>=@slider_low_range and year<=@slider_high_range")

	if selected_pollutant != "All":
		filtered_data = filtered_data[filtered_data["Prominent Pollutant"]==selected_pollutant]

	source.data = ColumnDataSource.from_df(filtered_data)

date_range.on_change("value", lambda attr, old, new: update_chart())
pollutant_select.on_change("value", lambda attr, old, new: update_chart())

# Layout
layout = column(row(date_range, pollutant_select), p)

curdoc().add_root(layout)
curdoc().title = "AQI Dashboard"