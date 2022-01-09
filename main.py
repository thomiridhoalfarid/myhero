"""Generate an interactive webapp using Bokeh to graph US economic data.

   The graph is generated and embedded into the template html file
     /templates/index.html
"""

from bokeh.layouts import row, column, widgetbox       #For laying out the page
from bokeh.models import TextInput, Button, Select, Div  #Interactive Widgets
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import curdoc, figure
import pandas as pd

from get_data import get_data

#------------------------------------------------------------------------------
#Some default settings:

GRAPH_WIDTH = 600
GRAPH_HEIGHT = 400
XLABEL = "Date"
YLABEL = "Value"

POPULAR_SERIES = { 'Real GDP'              : 'GDPC1', 
                   'Unemployment Rate'     : 'UNRATE', 
                   'CPI'                   : 'CPIAUCSL', 
                   '10 Year Treasury Rate' : 'DGS10'}

DEFAULT_SERIES = POPULAR_SERIES['Real GDP']
DEFAULT_START  = "1951-11-01"
DEFAULT_END    = "2016-11-1"

PAGE_TITLE = "Economic Data Graph"
#------------------------------------------------------------------------------

#Important:
#  Load data to be graphed into global variable source.  Note that source is of
#  type ColumnDataSource, the Bokeh data type (similar to a Pandas dataframe).
#  If you skip this step, the graph may respond slowly to changes.
#
#  First, load default data for default graph--the user can change that later
#  by interacting with the page through the widgets.
source = get_data(DEFAULT_SERIES, DEFAULT_START, DEFAULT_END)


#Add HoverTools to display values on the plot wherever the user hovers with
#the mouse. @values means display data from 'values' column of source,
#"Values" is the label to show in the tooltip.
hover = HoverTool(tooltips=[("Value", "@values")])


def make_plot(**kwargs):
  """Make the Bokeh plot to be displayed."""

  #Note: HoverTools is specified via hover
  p = figure(x_axis_type="datetime", plot_height=GRAPH_HEIGHT, \
    plot_width=GRAPH_WIDTH, tools=[hover], **kwargs)

  p.xaxis.axis_label = XLABEL
  p.yaxis.axis_label = YLABEL

  #Important: note that we specify source as the data source, and specify
  #column names 'date', 'values' from source to be graphed.
  p.line(x='date', y='values', source=source)
  return p


def update():
  """Update source variable holding data that the graph displays.

     Important note: callback functions like update() which are called by
     .on_click() events must take no arguments.
  """

  #Grab settings from widgets in the webapp's user interface:
  series = series_widget.value
  start = start_widget.value
  end = end_widget.value

  #Handle exceptions due to invalid inputs
  try:
    #reload data using the user preferences from the webapp's user interface
    src = get_data(series, start, end)

    source.data = src.data  #load data into source.data: graph will update
    div_widget.text = ""    #clear error messages

  except KeyboardInterrupt:
    return #don't catch these
  except ValueError as e:
    #Display error message in the page in the div_widget (html div)
    div_widget.text = "<h2>An error occured: {}</h2>".format(str(e))
  except Exception as e:
    errMsg = "<h2>An unexpected error occured with error message: <br>"
    errMsg += "{}</h2>".format(str(e))
    div_widget.text = errMsg


def pick_popular_series(attr, old, new):
  """Update the series & plot when user selects a series with Select widget.

     Important note: callback functions like pick_popular_series() which are
     called by .on_change() events must take arguments (attr, old, new).
  """
  #Update the series
  seriesCode = POPULAR_SERIES[pop_series_widget.value]
  series_widget.value = seriesCode

  #Update the plot
  update()

#------------------------------------------------------------------------------
#Layout the webapp page to be generated:

#First create interactive widgets:

#Text boxes for user input
series_widget = TextInput(title="Data series name", value=DEFAULT_SERIES)
start_widget  = TextInput(title="Start date", value=DEFAULT_START)
end_widget    = TextInput(title="End date", value=DEFAULT_END)

#Use this Div widget to create an html <div> block to display error messages
#to the user
div_widget = Div(text="", width=400, height=100)

#Button to regraph data
button_widget = Button(label="Graph", button_type="success")
button_widget.on_click(update)  #add .on_click handler

#Drop down selector to select popular economic data series
pop_series_widget = Select(title='Popular series',  \
  options=sorted(POPULAR_SERIES.keys()), value='Real GDP')
pop_series_widget.on_change('value', pick_popular_series) #add .on_change


#Create a widget-box: a group of widgets stacked vertically.
controls = widgetbox([series_widget, pop_series_widget, start_widget, \
  end_widget, button_widget], width=200)

#Layout the page: use column(a, b) to lay out items a over b in a column.
#Use row(c,d) to lay items c, d in a row
layout = column(row(controls, make_plot()), div_widget)

curdoc().add_root(layout)
curdoc().title = PAGE_TITLE     #webpage title
