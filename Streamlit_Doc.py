import streamlit as st
# #4
# st.altair_chart #done
# st.audio #done
# st.__annotations__ #pending
# #6
# st.balloons #pending
# st.bar_chart #done
# st.bokeh_chart #done
# st.button #pending
# st._bottom #pending
# st.__builtins__ #pending
# #15
# st.cache_data
# st.cache_resource
# st.caption
# st.camera_input
# st.chat_input
# st.chat_message
# st.checkbox
# st.code
# st.color_picker
# st.column_config
# st.columns
# st.container
# st.cache
# st.__cached__
# #7
# st.data_editor
# st.dataframe
# st.date_input
# st.divider
# st.download_button
# st.__dict__
# st.__doc__
# #14
# st.echo
# st.experimental_fragment
# st.empty
# st.exception
# st.expander
# st.experimental_data_editor
# st.experimental_connection
# st.experimental_get_query_params
# st.experimental_singleton
# st.experimental_user
# st.experimental_memo
# st.experimental_rerun
# st._event
# st.experimental_singleton
# st.experimental_rerun
# #4
# st.file_uploader
# st.form
# st.form_submit_button
# st.__file__
# #2
# st.get_option
# st.graphviz_chart
# #3
# st.header
# st.help
# st.html
# #2
# st.image
# st.info
# #1
# st.json
# #4
# st.latex
# st.line_chart
# st.link_button
# st.__loader__
# #5
# st.map
# st.markdown
# st.metric
# st.multiselect
# st._main
# #2
# st.number_input
# st.__name__
# #8
# st.page_link
# st.plotly_chart
# st.popover
# st.progress
# st.pydeck_chart
# st.__package__
# st.__path__
# st.pyplot
# #1
# st.query_params
# #2
# st.radio
# st.rerun
# #15
# st.scatter_chart
# st.secrets
# st.select_slider
# st.selectbox
# st.session_state
# st.set_option
# st.slider
# st.set_page_config
# st.snow
# st.status
# st.stop
# st.switch_page
# st.subheader
# st.success
# st.__spec__
# #9
# st.table
# st.tabs
# st.text
# st.text_area
# st.text_input
# st.time_input
# st.title
# st.toast
# st.toggle
# #1
# st._update_logger
# #3
# st.vega_lite_chart
# st.video
# st.__version__
# #3
# st.warning
# st.write
# st.write_stream
# #

# 1. st.write
st.subheader('1.st.write')
import streamlit as st

st.write('Hello, *World!* :sunglasses:')

import streamlit as st
import pandas as pd

st.write(1234)
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))
import streamlit as st

st.write('1 + 1 = ', 2)
st.write('Below is a DataFrame:', 'Above is a dataframe.')

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.write(c)