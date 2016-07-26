# import numpy as np

# from bokeh.io import curdoc
# from bokeh.layouts import row, widgetbox,layout
# from bokeh.models import ColumnDataSource, WidgetBox, CustomJS, TapTool
# from bokeh.models.widgets import Slider, TextInput
# from bokeh.plotting import figure,show, output_file

# from fit_data import *
# from utils import *

# detunings, transmission = get_data('data/p400uw_144_reduced.gpt')
# T = 130.0+273.15
# freq_centers = [-0.12, 0.0, 3.0, 6.0]
# x, _= multiple_profile(T, freq_centers, np.asarray(detunings)/1e3)
# source = ColumnDataSource(data=dict(x = detunings, y=x))

# def compute_error(transmission, x, detunings):
#     error = np.sum((np.asarray(transmission)-x)**2)/(np.sqrt(len(detunings)-5))
#     return str(error)

# def compute_densities(T):
#     return str(atomic_density(T)/1e6)

# plot = figure(plot_height = 600, plot_width = 800, title = "Testing with Bokeh",
#              tools = 'pan, reset, save, wheel_zoom,tap')

# plot.line(detunings, transmission, line_width = 3, line_alpha = 0.6)
# plot.line('x', 'y', source = source, line_width = 3, line_alpha = 0.6, line_color = 'red')


# plot.xaxis.axis_label = 'Detunings (MHz)'
# plot.yaxis.axis_label = 'Transmission (a.u)'

# # Setting up the widgets

# text = TextInput(title="title", value="Test for Bokeh")


# residue = TextInput(title="Mean Squared Error", value = compute_error(transmission,x,detunings))

# densities = TextInput(title = "Atomic Density (/cm^3)", value = compute_densities(T))

# temp_slider = Slider(title="Temperature", value = 130.0, start = 0.0, end = 200.0, step = 0.1, callback_policy = 'mouseup')
# center_1 = Slider(title = "Center 1", value = 0.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
# center_2 = Slider(title = "Center 2", value = 0.12, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
# center_3 = Slider(title = "Center 3", value = 3.0, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')
# center_4 = Slider(title = "Center 4", value = 6.8, start = -10.0, end = 10.0, step = 0.05, callback_policy = 'mouseup')

#     # Update title
# def update_title(attrname, old, new):
#     plot.title.text = text.value

# text.on_change('value', update_title)

# def update_data(attrname, old,new):
#     T = temp_slider.value+273.15
#     c1,c2,c3,c4 = center_1.value, center_2.value, center_3.value, center_4.value
#     freq_centers = [c1,c2,c3,c4]
#     x, _ = multiple_profile(T,freq_centers,np.asarray(detunings)/1e3)
#     x = normalize(x)
#     source.data = dict(x=detunings, y = x)
#     residue.value = compute_error(transmission,x,detunings)
#     densities.value = compute_densities(T)

# for w  in [temp_slider, center_1, center_2, center_3, center_4]:
#     w.on_change('value', update_data)

# inputs = WidgetBox(text, temp_slider, center_1, center_2, center_3, center_4, residue, densities)

# # # sliders = [temp_slider, center_1, center_2, center_3, center_4]
# # # l = layout([[text], [inputs, plot]])

# # output_server("test")
# # show(plot)

# # output_file("test.html", title="first_test")

# # show(l)

# l = layout([[inputs,plot],])

# curdoc().add_root(l)
# curdoc().title = "Non Linear Fit"

# # resources  = INLINE

# # js_resources = resources.render_js()
# # css_resources = resources.render_css()



# # # ## Embed HTML Code

# # template = Template( '''
# #     <!DOCTYPE html>
# #     <html lang="en">
# #     <head>
# #         <meta charset="utf-8">
# #         <title>Bokeh Scatter Plots</title>
# #         <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.css" type="text/css" />
# #         <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.css" type="text/css" />

# #         <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.js"></script>
# #         <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.js"></script>
# #         {{ plot_script }}
# #     </head>
# #     <body>
# #         {{ plot_div }}
# #     </body>
# # </html>
# # ''')

# # html = template.render(js_resources = js_resources,
# #                     css_resources = css_resources,
# #                     plot_script = script, plot_div = div)

# # filename = "embed_plot_with_widget.html"

# # with open(filename, 'w') as f:
# #     f.write(html.encode('utf-8'))


# # view(filename)



# # # # <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.css" type="text/css" />
# # # #         <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.css" type="text/css" />

# # # #         <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.0.min.js"></script>
# # # #         <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.0.min.js"></script>


from fit_data import *
from utils import *

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox,layout
from bokeh.models import ColumnDataSource, WidgetBox
from bokeh.models.widgets import Slider, TextInput, Button
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
divide = len(sas)/10
sas_clip = []
ramp_clip = []

for i in range(divide):
    sas_clip.append(np.average(sas[10*i:10*(i+1)]))
    ramp_clip.append(np.average(ramp[10*i:10*(i+1)]))

source_sas = ColumnDataSource(data=dict(x=range(len(sas_clip)), y=sas_clip))
source_ramp = ColumnDataSource(data=dict(x=range(len(ramp_clip)), y = ramp_clip))

plot = figure(plot_height = 600, plot_width = 800, title = "Rescaling Test",
             tools = 'pan, reset, save, wheel_zoom,hover, box_zoom')

plot.line('x', 'y', source = source_sas, line_width = 3, line_alpha = 0.6, line_color = 'red')
plot.line('x', 'y', source = source_ramp, line_width = 3, line_alpha = 0.6, line_color = 'green')


start_input = TextInput(title = "Starting Index for Clipping", value = str(0))
end_input = TextInput(title="End Index for Clipping", value = str(len(sas_clip)))
# command_box = TextInput(title="Enter Command", value="None")

center_1_input = TextInput(title = "Center for Rb87, lower transition", value = str(0))
center_2_input = TextInput(title = "Center for Rb87, upper transition", value = str(100))


clip_button = Button(label = "Clip", button_type="success")
rescale_button = Button(label = "Rescale", button_type = "success")

start = int(start_input.value)
end = int(end_input.value)

center_1 = int(center_1_input.value)
center_2 = int(center_2_input.value)

def update_inputs(attrname, old, new):
    start = int(start_input.value)
    end = int(end_input.value)

for w in [start_input, end_input]:
    w.on_change('value', update_inputs)

def update_plot():
    # command = command_box.value
    start = int(start_input.value)
    end = int(end_input.value)
    temp_sas = source_sas.data['y'][:]
    temp_ramp = source_ramp.data['y'][:]
    temp_sas = temp_sas[start:end]
    temp_ramp = temp_ramp[start:end]
    source_sas.data = dict(x=range(len(temp_sas)), y = temp_sas)
    source_ramp.data = dict(x = range(len(temp_ramp)), y = temp_ramp)
    # if command == "clip":
    #     temp_sas = source_sas.data['y'][:]
    #     temp_ramp = source_ramp.data['y'][:]
    #     temp_sas = temp_sas[start:end]
    #     temp_ramp = temp_ramp[start:end]
    #     source_sas.data = dict(x=range(len(temp_sas)), y = temp_sas)
    #     source_ramp.data = dict(x = range(len(temp_ramp)), y = temp_ramp)
    # else:
    #     pass

    start_input.value = str(0)
    end_input.value = str(len(source_sas.data['y']))


clip_button.on_click(update_plot)

def rescale(start_index, end_index):
    freq_difference = 6.834e9
    frequencies = []
    slope = freq_difference/(end_index-start_index)
    for i in range(len(source_sas.data['y'])):
        frequencies.append(slope*(i-start_index)+384.22811e12);
    print len(frequencies)
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


rescale_button.on_click(update_rescale)


inputs = WidgetBox(start_input, end_input,clip_button, center_1_input, center_2_input, rescale_button)


l = layout([[inputs,plot],])

curdoc().add_root(l)
curdoc().title = "Rescale Test"








