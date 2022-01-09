"""Add your code here to retrieve data and return for plotting:"""

from bokeh.models import ColumnDataSource

import pandas as pd
import pandas_datareader.data as web

def get_data(series_name, start_date, end_date):
  """Returns Bokeh ColumnDataSource holding data to be graphed.

  Pulls economics data series (series_name) from the Federal Reserve Database
  (FRED) using pandas_datareader.

  Args:
    series_name: string, like "GDPC1", specifies economics data series from
      the FRED database.  Look up more series here: https://fred.stlouisfed.org/
    start_date: string, like "1951-11-01", start date of data to grab
    end_date: string, like "2016-11-1", end date of data to grab

  Returns:
    ColumnDataSource with econ time series data to graph.  Column 'date' holds
    the date of each point and column 'values' holds the series values.

  Raises:
    ValueError: if inputs series_name, start_date, or end_date are invalid.
      ValueError may also be raised if the network connection fails.
  """

  try:
    start = pd.to_datetime(str(start_date).strip())
  except KeyboardInterrupt:  #don't catch these
    return
  except:
    raise ValueError("Start date is not formatted correctly.")

  try:
    end = pd.to_datetime(str(end_date).strip())
  except KeyboardInterrupt:
    return
  except:
    raise ValueError("End date is not formatted correctly.")

  #Grab data from FRED. DataReader returns a Pandas dataframe df.
  try:
    df = web.DataReader(str(series_name).strip(), "fred", start, end)
  except KeyboardInterrupt:
    return
  except:
    raise ValueError("Data retrieval failed. Double check that the "+\
      "series is valid. If it's valid, check your internet connection.")


  df.columns = ['values'] #rename column
  df['date'] = df.index   #add date column
  df.dropna(inplace=True) #drop any rows with missing data

  #Convert pandas dataframe to ColumnDataSource (Bokeh's native data format)
  return ColumnDataSource(data=df)
