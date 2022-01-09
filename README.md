# Interactive Bokeh webapp to view US economic data

As a demonstration, in this example I modified the web app template 
(from *1_AppTemplate/*) to build an
interactive website to graph US economic data from the Federal
Reserve.  

In `get_data.py`, I modified the function `get_data()` to 
load economic data over the internet using pandas_datareader.

In `main.py`, I modified the design of the interactive webapp to
add custom textboxes and buttons.

Inside *templates*, I changed the 
template html file  `index.html` to add custom text and links.