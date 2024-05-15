import streamlit as st
import altair as alt
import pandas as pd

# Sample data
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5,6],
    'y': [34, 22, 23, 23, 22,27]
})

# Create Altair chart
chart = alt.Chart(data).mark_line().encode(
    x='x',
    y='y'
)

# Render Altair chart in Streamlit app
st.altair_chart(chart, use_container_width=True)
