import numpy as np

from bokeh.io import curdoc, output_file, show
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import ColumnDataSource, WidgetBox
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure


output_file("test.html")

N = 200
x = np.linspace(0,4*np.pi, N)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x,y=y))

#Setting up the plot

plot = figure(plot_height=400, plot_width=400, title="Sliders Test",
	tools ="crosshair, pan, reset, save, wheel_zoom",
	x_range=[0,4*np.pi], y_range=[-2.5,2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

#Set up the widgets

text = TextInput(title="title", value= "my sine wave");
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start = 0.1, end = 5.1)

# Set up callbacks

def update_title(attrname, old, new):
	plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

	# Get the current slider values
	a = amplitude.value
	b = offset.value
	w = phase.value
	k = freq.value

	# Generate the new curve
	x = np.linspace(0,4*np.pi, N)
	y = a*np.sin(k*x+w) + b

	source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq] :
	w.on_change('value', update_data)

# Set up layouts

# inputs = widgetbox(text, offset, amplitude, phase, freq)
inputs = WidgetBox(text, offset, amplitude, phase, freq)

# # l = layout(row(inputs, plot, width=800))

# curdoc().add_root(row(inputs, plot, width=800))
# curdoc().title = "Sliders"
l = layout([[inputs,plot],])

show(l)


## Clearly a problem with the html generated. I think it doesnt load the js necessary for the widget control
## Need to create some sort of external javascript to be able to run the widget code
