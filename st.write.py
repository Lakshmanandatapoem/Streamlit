import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['d', 'g', 'h'])

c = alt.Chart(df).mark_circle().encode(
    x='d', y='g', size='d', color='h', tooltip=['d', 'g', 'h'])

st.write(c)

