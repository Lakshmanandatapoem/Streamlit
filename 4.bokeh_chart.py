import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


x = [1, 2, 3, 4, 5]
y = [3, 6, 2, 8, 9]

p = figure(title="Simple Line Plot", x_axis_label='x', y_axis_label='y')

p.line(x, y, legend_label="Line", line_width=2)

st.bokeh_chart(p, use_container_width=True)
