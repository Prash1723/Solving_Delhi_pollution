import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, RangeSlider
from bokeh.models.widgets import RadioGroup, Toggle
from bokeh.models import Tabs, TabPanel
from bokeh.plotting import figure

import logging
from rich.console import Console
from rich.logging import RichHandler

rc = Console(record=True)

# Set up the logger
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# 1. Console Handler (Rich)
shell_handler = RichHandler()
log.addHandler(shell_handler)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(file_handler)

df = pd.read_csv(r'~/Projects/Solving_Delhi_pollution/data/preprocessed.csv')
df['date'] = pd.to_datetime(df['date'])
df['Prominent Pollutant'] = df['Prominent Pollutant'].astype('str')
print(df.info())


try:
	# Source
	source1 = ColumnDataSource(df)

	# Create widgets
	date_range = RangeSlider(
		title="Select range of year",
		value=(2015, 2023),
		start=2015,
		end=2023,
		step=1
		)

	radio_pollutant = RadioGroup(
		labels=["combo", "individual"],
		active=0
		)

	combo_select = Select(
		title="Select Pollutant combination",
	    value="All",
		options=["All"] + list(set(df['Prominent Pollutant']))
		)


	pollutant_select = Select(
		title="Select Pollutant combination",
	    value="OZONE",
		options=['SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']
		)

	# Figure - Time series(all pollutants)
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

	# Figure - Time series(Singular pollutant)
	p2 = figure(
		x_axis_type="datetime",
		title="AQI(Pollutant) trend line",
		height=400,
		width=700
		)

	p2.line("date", "Index Value", source=source1, line_width=2)
	p2.scatter("date", "Index Value", source=source1, size=3, color="red")
	p2.xaxis.axis_label = "Date"	
	p2.yaxis.axis_label = "AQI Value"

	# App
	def update_chart():
		slider_value = date_range.value
		slider_lr = slider_value[0]
		slider_hr = slider_value[1]

		selected_combo = combo_select.value

		if selected_combo != "All":
			filtered_data = df.query('year>=@slider_lr and year<=@slider_hr')[df["Prominent Pollutant"]==selected_combo]
			source1.data = filtered_data
			source1.change.emit()

		else:
			source1.data = df.query('year>=@slider_lr and year<=@slider_hr')

	def update_chartp2(attr, old, new):
		selected_pollutant = pollutant_select.value
		slider_lr = slider_value[0]
		slider_hr = slider_value[1]

		if selected_pollutant in ['SO2', 'NO2', 'O3', 'PM10', 'CO', 'OZONE', 'PM2.5']:
			filtered_data = df.query('year>=@slider_lr and year<=@slider_hr')[df[selected_pollutant]==1]
			source1.data = filtered_data
			source1.change.emit()

	radio_pollutant.on_change("active", toggle_polchart)
	date_range.on_change("value", lambda attr, old, new: update_chart())
	combo_select.on_change("value", lambda attr, old, new: update_chart())
	pollutant_select.on_change("value", lambda attr, old, new: update_chart())

	# Layout
	layout = column(row(date_range, combo_select, radio_pollutant, pollutant_select), p)

	curdoc().add_root(layout)
	curdoc().title = "AQI Dashboard"

except Exception as e:
	log.info(f"Error: {e}")