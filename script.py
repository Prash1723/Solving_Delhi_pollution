import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, RangeSlider
from bokeh.models import Tabs, TabPanel
from bokeh.plotting import figure

df = pd.read_csv(r'~/Projects/Solving_Delhi_pollution/data/preprocessed.csv')

df['date'] = pd.to_datetime(df['date'])
# df['year'] = df['date'].dt.year

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

season_select = Select(
	title="Select Season",
	value="All",
	options=["All"] + list(set(df['season'].dropna().astype(str)))
	)

agg_season_select = Select(
	title="Select Agg.",
	value="average",
	options=["average", "minimum", "maximum"]
	)

# Figure
p = figure(
	x_axis_type="datetime",
	title="AQI trend line",
	height=500,
	width=900
	)

p.line("date", "Index Value", source=source1, line_width=2)
p.scatter("date", "Index Value", source=source1, size=3, color="red")
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "AQI Value"

# Pollutants present
pollutants = ['SO2', 'O3', 'PM10', 'NO2', 'OZONE', 'CO', 'PM2.5']

df2 = df[["SO2", "O3", "PM10", "NO2", "OZONE", "CO", "PM2.5"]].sum().reset_index()

df2.columns = ['pollutants', 'days']

source2 = ColumnDataSource(df2)

p2 = figure(
	x_range=(0,3000),
	y_range=pollutants,
	title="No. of days pollutants present",
	height=250,
	width=400
	)

p2.hbar( 
	y='pollutants', 
	right='days', 
	height=0.5, 
	source=source2
	)

p2.text(
	x='days',
	y='pollutants',
	text='days',
	x_offset=5,
	y_offset=5,
	text_color='white',
	anchor='bottom_left',
	source=source2
	)

p2.xaxis.axis_label = "Days"
p2.yaxis.axis_label = "Pollutants"

# Air quality

aq = df['Air Quality'].unique().tolist()

df3 = df.groupby('Air Quality')['date'].count().reset_index()

df3.columns = ['Air Quality', 'days']

source3 = ColumnDataSource(df3)

p3 = figure(
	x_range=(0,1500),
	y_range=aq,
	title="Quality of Air in days",
	height=250,
	width=400
	)

p3.hbar( 
	y='Air Quality', 
	right='days', 
	height=0.5, 
	source=source3
	)

p3.text(
	x='days',
	y='Air Quality',
	text='days',
	x_offset=5,
	y_offset=5,
	text_color='white',
	anchor='bottom_left',
	source=source3
	)

p3.xaxis.axis_label = "Days"
p3.yaxis.axis_label = "Air Quality"

# Seasons

se = df['season'].unique().tolist()

df4 = round(df.groupby('season')['Index Value'].mean(), 2).reset_index()

df4.columns = ['season', 'aqi']

source4 = ColumnDataSource(df4)

p4 = figure(
	x_range=(0,600),
	y_range=se,
	title="AQI by seasons",
	height=250,
	width=400
	)

p4.hbar( 
	y='season', 
	right='aqi', 
	height=0.5, 
	source=source4
	)

p4.text(
	x='aqi',
	y='season',
	text='aqi',
	x_offset=5,
	y_offset=5,
	text_color='white',
	anchor='bottom_left',
	source=source4
	)

p4.xaxis.axis_label = "Index Value"
p4.yaxis.axis_label = "season"

# Monthly chart

mc = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

df5 = round(df.groupby('month')['Index Value'].mean(), 2).reset_index()

df5.columns = ['month', 'aqi']

source5 = ColumnDataSource(df5)

p5 = figure(
	y_range=(0,600),
	x_range=mc,
	title="AQI by months",
	height=250,
	width=800
	)

p5.vbar( 
	x='month', 
	top='aqi', 
	width=0.5,
	source=source5
	)

p5.text(
	y='aqi',
	x='month',
	text='aqi',
	x_offset=5,
	y_offset=-10,
	text_color='white',
	angle=0,
	anchor='bottom',
	source=source5
	)

p5.yaxis.axis_label = "Index Value"
p5.xaxis.axis_label = "month"

# Monthly quality chart

df6 = df.groupby(['month', 'Air Quality'])['date'].count().reset_index()

df6.columns = ['month', 'aq', 'days']

source6 = ColumnDataSource(df6)

p6 = figure(
        y_range=(0,250),
        x_range=mc,
        title="monthly aq",
        height=250,
        width=800
        )

p6.vbar( 
        x='month', 
        top='days', 
        width=0.5,
        source=source6,
        legend_field='aq'
        )

p6.text(
        y='days',
        x='month',
        text='days',
        x_offset=5,
        y_offset=-10,
        text_color='white',
        angle=0,
        anchor='bottom',
        source=source6
        )

p6.yaxis.axis_label = "days"
p6.xaxis.axis_label = "month"

# App
def update_chart1():
	slider_value = date_range.value
	slider_lr = slider_value[0]
	slider_hr = slider_value[1]
	selected_pollutant = pollutant_select.value
	selected_season = season_select.value
	selected_agg_season = agg_season_select.value

	# Trend line
	if selected_pollutant != "All" and selected_season != "All":
		# Trend line
		filtered_data1 = df.query(
			"`Prominent Pollutant` == @selected_pollutant and season == @selected_season and year>=@slider_lr and year<=@slider_hr"
			)

		# Pollutant presence
		filtered_data2 = df.query(
			"`Prominent Pollutant` == @selected_pollutant and season == @selected_season and year>=@slider_lr and year<=@slider_hr"
			)[[
		"SO2",
		"O3",
		"PM10",
		"NO2", 
		"OZONE", 
		"CO", 
		"PM2.5"
		]].sum().reset_index()

		filtered_data2.columns = ['pollutants', 'days']

		# Air Quality
		filtered_data3 = df.query(
			"`Prominent Pollutant` == @selected_pollutant and season == @season_select and year>=@slider_lr and year<=@slider_hr"
			).groupby('Air Quality')[
		'date'
		].count().reset_index()

		filtered_data3.columns = ['Air Quality', 'days']

	elif selected_pollutant == "All" and selected_season != "All":
		# Trend line
		filtered_data1 = df.query("season == @selected_season and year>=@slider_lr and year<=@slider_hr")

		# Pollutant presence
		filtered_data2 = df.query("season == @selected_season and year>=@slider_lr and year<=@slider_hr")[[
		"SO2",
		"O3",
		"PM10",
		"NO2", 
		"OZONE", 
		"CO", 
		"PM2.5"
		]].sum().reset_index()

		filtered_data2.columns = ['pollutants', 'days']

		# Air Quality
		filtered_data3 = df.query("season == @selected_season and year>=@slider_lr and year<=@slider_hr").groupby('Air Quality')[
		'date'
		].count().reset_index()

		filtered_data3.columns = ['Air Quality', 'days']

	elif selected_pollutant != "All" and selected_season == "All":
		# Trend line
		filtered_data1 = df.query("`Prominent Pollutant` == @selected_pollutant and year>=@slider_lr and year<=@slider_hr")

		# Pollutant presence
		filtered_data2 = df.query("`Prominent Pollutant` == @selected_pollutant and year>=@slider_lr and year<=@slider_hr")[[
		"SO2",
		"O3",
		"PM10",
		"NO2", 
		"OZONE", 
		"CO", 
		"PM2.5"
		]].sum().reset_index()

		filtered_data2.columns = ['pollutants', 'days']

		# Air Quality
		filtered_data3 = df.query(
			"`Prominent Pollutant` == @selected_pollutant and year>=@slider_lr and year<=@slider_hr"
			).groupby('Air Quality')[
		'date'
		].count().reset_index()

		filtered_data3.columns = ['Air Quality', 'days']

	else:
		# Trend line(--All--)
		filtered_data1 = df.query("year >= @slider_lr and year <= @slider_hr")

		# Pollutant presence(--All--)
		filtered_data2 = df.query("year >= @slider_lr and year <= @slider_hr")[[
		"SO2",
		"O3",
		"PM10",
		"NO2", 
		"OZONE", 
		"CO", 
		"PM2.5"
		]].sum().reset_index()

		filtered_data2.columns = ['pollutants', 'days']

		# Air Quality(--All--)
		filtered_data3 = df.query("year >= @slider_lr and year <= @slider_hr").groupby('Air Quality')[
		'date'
		].count().reset_index()

		filtered_data3.columns = ['Air Quality', 'days']

	# Seasonality
	if selected_agg_season == 'average':
		# Seasons
		filtered_data4 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('season')[
		'Index Value'
		].mean(), 2).reset_index()

		# Months
		filtered_data5 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('month')[
		'Index Value'
		].mean(), 2).reset_index()

	elif selected_agg_season == 'minimum':
		# Seasons
		filtered_data4 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('season')[
		'Index Value'
		].min(), 2).reset_index()

		# Months
		filtered_data5 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('month')[
		'Index Value'
		].min(), 2).reset_index()

	else:
		# Seasons
		filtered_data4 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('season')[
		'Index Value'
		].max(), 2).reset_index()

		# Months
		filtered_data5 = round(df.query("year>=@slider_lr and year<=@slider_hr").groupby('month')[
		'Index Value'
		].max(), 2).reset_index()

	# Monthly air quality
	filtered_data6 = df.query(
 		"year>=@slider_lr and year<=@slider_hr"
 		).groupby(['month', 'Air Quality'])['date'].count().reset_index()

	filtered_data4.columns = ['season', 'aqi']
	filtered_data5.columns = ['month', 'aqi']
	filtered_data6.columns = ['month', 'aq', 'days']

	source1.data = ColumnDataSource.from_df(filtered_data1)
	source2.data = ColumnDataSource.from_df(filtered_data2)
	source3.data = ColumnDataSource.from_df(filtered_data3)
	source4.data = ColumnDataSource.from_df(filtered_data4)
	source5.data = ColumnDataSource.from_df(filtered_data5)
	source6.data = ColumnDataSource.from_df(filtered_data6)

date_range.on_change("value", lambda attr, old, new: update_chart1())
pollutant_select.on_change("value", lambda attr, old, new: update_chart1())
season_select.on_change("value", lambda attr, old, new: update_chart1())
agg_season_select.on_change("value", lambda attr, old, new: update_chart1())

# Layout
layout = row(
	row(
		column(
			row(date_range, pollutant_select, season_select), 
			row(p, column(p2, p3)
			), 
			column(
				agg_season_select,  
				row(p4, p5), 
				p6
				)
			)
		)
	)

curdoc().add_root(layout)
curdoc().theme = 'night_sky'
curdoc().title = "AQI Dashboard"