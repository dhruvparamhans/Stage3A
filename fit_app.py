from fit_data import *
from utils import *

import numpy as np

from bokeh.io import curdoc, show
from bokeh.layouts import row, widgetbox,layout
from bokeh.models import ColumnDataSource, WidgetBox
from bokeh.models.widgets import Slider, TextInput, Button, Select
from bokeh.plotting import figure,show, output_file
import csv

import glob
filenames = glob.glob('data/*.csv')

filename = filenames[0]
spectra, reference, sas, ramp = get_csv(filename,factor=100)


source_spectra = ColumnDataSource(data = dict(x = range(len(spectra)), y = spectra))
source_fit = ColumnDataSource(data = dict(x = range(len(reference)), y = []))

source_sas = ColumnDataSource(data=dict(x=range(len(sas)), y=sas))
source_ramp = ColumnDataSource(data=dict(x=range(len(ramp)), y = ramp))

plot1 = figure(plot_height = 400, plot_width = 600, title = "Rescaling",
                 tools = 'pan, reset, save, wheel_zoom,hover, box_zoom')

plot_sas = plot1.line('x', 'y', source = source_sas, line_width = 3, line_alpha = 0.6, line_color = 'red')
plot_ramp = plot1.line('x', 'y', source = source_ramp, line_width = 3, line_alpha = 0.6, line_color = 'green')


plot2 = figure(plot_height = 400, plot_width = 600, title = "Fit",
                    tools = 'pan, reset, save, wheel_zoom, hover, box_zoom')

plot_spectra = plot2.line('x', 'y', source = source_spectra, line_width = 3, line_alpha=0.6, line_color = 'blue')
plot_fit = plot2.line('x', 'y', source = source_fit, line_width = 3, line_alpha = 0.6, line_color = 'red')


## Create Widgets
start_input = TextInput(title = "Starting Index for Clipping", value = str(0))
end_input = TextInput(title="End Index for Clipping", value = str(len(sas)))
center_1_input = TextInput(title = "Center for Rb87, lower transition", value = str(0))
center_2_input = TextInput(title = "Center for Rb87, upper transition", value = str(100))
clip_button = Button(label = "Clip", button_type="success")
rescale_button = Button(label = "Rescale", button_type = "success")
normalize_button = Button(label = "Normalize", button_type = "success")

start = int(start_input.value)
end = int(end_input.value)

center_1 = int(center_1_input.value)
center_2 = int(center_2_input.value)

temp_slider = Slider(title="Temperature", value = 130.0, start = 0.0, end = 200.0, step = 0.1, callback_policy = 'mouseup')
center_1 = Slider(title = "Center 1", value = 0.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_2 = Slider(title = "Center 2", value = 0.12, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_3 = Slider(title = "Center 3", value = 3.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
center_4 = Slider(title = "Center 4", value = 6.8, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')




## Update Callbacks
def update_inputs(attrname, old, new):
    start = int(start_input.value)
    end = int(end_input.value)

for w in [start_input, end_input]:
    w.on_change('value', update_inputs)

def update_plot():
    # command = command_box.value
    start = int(start_input.value)
    end = int(end_input.value)
    temp = source_sas.data['y'][:]
    temp = temp[start:end]
    source_sas.data = dict(x = range(len(temp)), y = temp)
    temp = source_ramp.data['y']
    temp = temp[start:end]
    source_ramp.data = dict(x = range(len(temp)), y = temp)
    temp = source_spectra.data['y']
    temp = temp[start:end]
    source_spectra.data = dict(x = range(len(temp)), y = temp)
    source_fit.data = dict(x = range(len(temp)), y = temp)
    start_input.value = str(0)
    end_input.value = str(len(source_sas.data['y']))
    start = int(start_input.value)
    end = int(end_input.value)

clip_button.on_click(update_plot)



def rescale(start_index, end_index):
    freq_difference = 6.834e9
    frequencies = []
    slope = freq_difference/(end_index-start_index)
    for i in range(len(source_sas.data['y'])):
        frequencies.append(slope*(i-start_index)+384.22811e12);
    center = frequencies[start_index]
    detunings = []
    for i in range(len(source_sas.data['y'])):
        detunings.append(frequencies[i] - center);
    return np.asarray(detunings)/1e6, frequencies


def update_rescale():
    start_index = int(center_1_input.value)
    end_index = int(center_2_input.value)
    dets, frequencies = rescale(start_index, end_index)
    temp = source_sas.data['y']
    source_sas.data = dict(x = dets, y = temp)
    temp = source_ramp.data['y']
    source_ramp.data = dict(x=dets, y = temp)
    temp = source_spectra.data['y']
    source_spectra.data = dict(x=dets, y = temp)
    source_fit.data = dict(x=dets, y = temp)

    plot1.xaxis.axis_label = "Detunings (MHz)"
    plot1.yaxis.axis_label = "Transmission (a.u.)"

    plot2.xaxis.axis_label = "Detunings (MHz)"
    plot2.yaxis.axis_label = "Transmission (a.u.)"


rescale_button.on_click(update_rescale)


def update_normalize():
    start = int(start_input.value)
    end = int(end_input.value)
    x = source_spectra.data['y']
    spectra_norm = renormalize(x)
    spectra_norm = normalize(spectra_norm)
    source_spectra.data['y'] = spectra_norm
    source_fit.data['y'] = spectra_norm


normalize_button.on_click(update_normalize)

detunings = source_spectra.data['x']
transmission = source_spectra.data['y']
T = 130.0+273.15
freq_centers = [-0.12, 0.0, 3.0, 6.0]
x, _= multiple_profile(T, freq_centers, np.asarray(detunings)/1e3)
source_fit.data = dict(x = detunings, y = x)

def compute_error(transmission, x, detunings):
    error = np.sum((np.asarray(transmission)-x)**2)/(np.sqrt(len(detunings)-5))
    return str(error)
def compute_densities(T):
    return str(atomic_density(T)/1e6)
residue = TextInput(title="Mean Squared Error", value = compute_error(transmission,x,detunings))

densities = TextInput(title = "Atomic Density (/cm^3)", value = compute_densities(T))

def update_data(attrname, old,new):
    detunings = source_spectra.data['x']
    transmission = source_spectra.data['y']
    T = temp_slider.value+273.15
    c1,c2,c3,c4 = center_1.value, center_2.value, center_3.value, center_4.value
    freq_centers = [c1,c2,c3,c4]
    x, _ = multiple_profile(T,freq_centers,np.asarray(detunings)/1e3)
    x = normalize(x)
    source_fit.data = dict(x = detunings, y = x)
    residue.value = compute_error(transmission,x,detunings)
    densities.value = compute_densities(T)

for w  in [temp_slider, center_1, center_2, center_3, center_4]:
    w.on_change('value', update_data)


## Final layout
column1 = WidgetBox(start_input, end_input, clip_button)
column2 = WidgetBox(center_1_input, center_2_input, rescale_button)
column3 = WidgetBox(residue,temp_slider,center_1, center_2)
column4 = WidgetBox(densities, center_3, center_4, normalize_button)


l = layout([[plot1,plot2],[column1,column2, column3,column4],])

curdoc().add_root(l)
curdoc().title = "Non Linear Absorption Fit"
