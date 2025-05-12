import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, RangeSlider
from bokeh.models import Tabs, TabPanel
from bokeh.plotting import figure

df = pd.read_csv(r'~/Projects/Solving_Delhi_pollution/data/Delhi_AQIBulletins.csv')

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

print(df['Prominent Pollutant'][23])

# Source
source1 = ColumnDataSource(df)

# Create widgets
date_range = RangeSlider(
	title="Select range of year",
	value=(df.year.min(), df.year.max()),
	start=df.year.min(),
	end=df.year.max(),
	step=1
	)

pollutant_select = Select(
	title="Select Pollutant",
    value="All",
	options=["All"] + list(set(df['Prominent Pollutant'].dropna().astype(str)))
	)

# Figure
p = figure(
	x_axis_type="datetime",
	title="AQI trend line",
	height=400,
	width=700
	)

p.line("date", "Index Value", source=source1, line_width=2)
p.scatter("date", "Index Value", source=source1, size=3, color="red")
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "AQI Value"

# App
def update_chart():
	slider_value = date_range.value
	slider_lr = slider_value[0]
	slider_hr = slider_value[1]
	selected_pollutant = pollutant_select.value

	if selected_pollutant != "All":
		filtered_data = df.query("`Prominent Pollutant` == @selected_pollutant and year >= @slider_lr and year <= @slider_hr")

	else:
		filtered_data = df.query("year>=@slider_lr and year<=@slider_hr")

	source1.data = ColumnDataSource.from_df(filtered_data)

date_range.on_change("value", lambda attr, old, new: update_chart())
pollutant_select.on_change("value", lambda attr, old, new: update_chart())

# Layout
layout = column(row(date_range, pollutant_select), p)

curdoc().add_root(layout)
curdoc().title = "AQI Dashboard"