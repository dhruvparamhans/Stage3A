from fit_data import *
from utils import *

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox,layout
from bokeh.models import ColumnDataSource, WidgetBox
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure,show, output_file
import csv


filename = 'data/p40uw_144_raw.csv'
data_list  =[]
fileReader  = csv.reader(open(filename), delimiter=' ')


for row in fileReader:
	x = map(lambda y: float(y), row)
	data_list.append(x)

sas = np.asarray(data_list)[:,4]
ramp = np.asarray(data_list)[:,3]

sas = list(reversed(sas))
ramp = list(reversed(ramp))
sas = normalize(sas)

## Divide number of points by 100
divide = len(sas)/100
sas_clip = []
ramp_clip = []

for i in range(divide):
	sas_clip.append(np.average(sas[100*i:100*(i+1)]))
	ramp_clip.append(np.average(ramp[100*i:100*(i+1)]))

source_sas = ColumnDataSource(data=dict(x=range(len(sas_clip)), y=sas_clip))
source_ramp = ColumnDataSource(data=dict(x=range(len(ramp_clip)), y = ramp_clip))

plot = figure(plot_height = 600, plot_width = 800, title = "Testing with Bokeh",
             tools = 'pan, reset, save, wheel_zoom,hover')

plot.line('x', 'y', source = source_sas, line_width = 3, line_alpha = 0.6, line_color = 'red')
plot.line('x', 'y', source = source_ramp, line_width = 3, line_alpha = 0.6, line_color = 'green')


start_input = TextInput(title = "Start", value = str(0))
end_input = TextInput(title="End", value = str(len(sas_clip)))
command_box = TextInput(title="Enter Command", value="None")

check_box = TextInput(title="For verification", value = " ")

start = int(start_input.value)
end = int(end_input.value)

print type(start)

def update_inputs(attrname, old, new):
	start = int(start_input.value)
	end = int(end_input.value)
	check_box.value = str(start)

for w in [start_input, end_input,check_box]:
	w.on_change('value', update_inputs)

def update_plot(attrname, old, new):
	command = command_box.value
	start = int(start_input.value)
	end = int(end_input.value)

	if command == "clip":
		temp_sas = source_sas.data['y'][:]
		temp_ramp = source_sas.ramp['y'][:]
		temp_sas = temp_sas[start:end]
		temp_ramp = temp_ramp[start:end]
		source_sas.data = dict(x=range(len(temp_sas)), y = temp_sas)
		source_ramp.data = dict(x = range(len(temp_ramp)), y = temp_ramp)
	else:
		pass

	start_input.value = str(0)
	end_input.value = str(len(source_sas.data['y']))


command_box.on_change('value', update_plot)


inputs = WidgetBox(start_input, end_input,command_box, check_box)


l = layout([[inputs,plot],])

curdoc().add_root(l)
curdoc().title = "Rescale Test"








