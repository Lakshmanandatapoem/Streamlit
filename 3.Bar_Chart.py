import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
   {"col1": list(range(15)), 
    "col2": np.random.randn(15), 
    "col3": np.random.randn(15)}
)

st.bar_chart(
   chart_data, x="col1", y=["col2", "col3"], 
   color=["#FF0000", "#FFA500"]
)