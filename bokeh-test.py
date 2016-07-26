import numpy as np

from bokeh.io import curdoc, output_notebook
from bokeh.layouts import row, widgetbox,layout
from bokeh.models import ColumnDataSource, WidgetBox
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure,show, output_file, output_server

from fit_data import *
from utils import *
# output_file('index.html')
# Get test data

detunings, transmission = get_data('data/p400uw_144_reduced.gpt')
T = 130.0+273.15
freq_centers = [-0.12, 0.0, 3.0, 6.0]
x, _= multiple_profile(T, freq_centers, np.asarray(detunings)/1e3)
source = ColumnDataSource(data=dict(x = detunings, y=x))

def compute_error(transmission, x, detunings):
    error = np.sum((np.asarray(transmission)-x)**2)/(np.sqrt(len(detunings)-5))
    return str(error)

def compute_densities(T):
    return str(atomic_density(T)/1e6)

plot = figure(plot_height = 600, plot_width = 800, title = "Testing with Bokeh",
             tools = 'pan, reset, save, wheel_zoom')

plot.line(detunings, transmission, line_width = 3, line_alpha = 0.6)
plot.line('x', 'y', source = source, line_width = 3, line_alpha = 0.6, line_color = 'red')

plot.xaxis.axis_label = 'Detunings (MHz)'
plot.yaxis.axis_label = 'Transmission (a.u)'

    # Setting up the widgets

text = TextInput(title="title", value="Test for Bokeh")

residue = TextInput(title="Mean Squared Error", value = compute_error(transmission,x,detunings))

densities = TextInput(title = "Atomic Density (/cm^3)", value = compute_densities(T))

temp_slider = Slider(title="Temperature", value = 130.0, start = 0.0, end = 200.0, step = 0.1, callback_policy = 'mouseup')
center_1 = Slider(title = "Center 1", value = 0.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_2 = Slider(title = "Center 2", value = 0.12, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_3 = Slider(title = "Center 3", value = 3.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_4 = Slider(title = "Center 4", value = 6.8, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')

    # Update title
def update_title(attrname, old, new):
    plot.title.text = text.value
text.on_change('value', update_title)

def update_data(attrname, old,new):
    T = temp_slider.value+273.15
    c1,c2,c3,c4 = center_1.value, center_2.value, center_3.value, center_4.value
    freq_centers = [c1,c2,c3,c4]
    x, _ = multiple_profile(T,freq_centers,np.asarray(detunings)/1e3)
    x = normalize(x)
    source.data = dict(x=detunings, y = x)
    residue.value = compute_error(transmission,x,detunings)
    densities.value = compute_densities(T)

for w  in [temp_slider, center_1, center_2, center_3, center_4]:
    w.on_change('value', update_data)

inputs = WidgetBox(text, temp_slider, center_1, center_2, center_3, center_4, residue, densities)

# # sliders = [temp_slider, center_1, center_2, center_3, center_4]
# # l = layout([[text], [inputs, plot]])

# output_server("test")
# show(plot)

# output_file("test.html", title="first_test")

# show(l)

l = layout([[inputs,plot],])

# show(l)

curdoc().add_root(l)
curdoc().title = "Test"
