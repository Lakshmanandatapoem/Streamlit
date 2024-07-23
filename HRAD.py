import streamlit as st
import pandas as pd
import time
import io
import os
import sys
import subprocess
import json
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvmYqBUHrak_oQF2Nt26-2c8ke9tbA39NfelFyPAjyIWToA99yJco-FwlmJxekCk2JzRs&usqp=CAU",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS for the background color and other styles
custom_css = """
<style>
/* Set the background color */
body {
    background-color: yellow ; /* Change this to your preferred color */
}

/* Reduce gap between elements */
div.stMarkdown {
    margin-top: 0;
    margin-bottom: 0;
}

hr {
    margin: 0;
}

/* Style the buttons */
div.stButton button {
    background-color: #3F51B5; /* Green */
    border: none;
    color: white;
    padding: 14px 14px; /* Adjusted padding */
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 17px; /* Adjusted font size */
    margin: 1px; /* Adjusted margin */
    cursor: pointer;
    border-radius: 17px;  /* Adjusted border-radius */
}

/* Change button color on hover */
div.stButton button:hover {
    background-color: #3F51B5;
}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Create a container for the title and buttons
with st.container():
    st.subheader("HR Analytics Dashboard")
    st.markdown("---")  # Add a horizontal divider
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col1:
        home_button = st.button("Home")
    with col2:
        Summary_button = st.button("Summary")
    with col3:
        Employees_Overview_button = st.button("Employees Overview")
    with col4:
        departments_button = st.button("Departments", key='departments')
    with col5:
        Salary_Analysis_button = st.button("Salary Analysis")
    with col6:
        hiring_and_termination_button = st.button("Hiring and Termination", key='hiring-termination')
    with col7:
        Training_button = st.button("Training")
    with col8:
        setting_button = st.button("Setting")
    with col9:
        more_feature_button = st.button("More Feature")
    st.markdown("---")

def login(username, password):
    # This function should be defined to handle login logic
    # For demonstration purposes, let's assume it always returns True
    return True

if home_button:
    st.write("Home")
elif Summary_button:
    st.write("Summary")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        # Display the DataFrame
        st.markdown("<hr>", unsafe_allow_html=True) 
        st.write(df)
        # Optionally, show the DataFrame's statistics
        st.write("Data Statistics:")
        st.write(df.describe())
        # Optionally, show a sample of the DataFrame
        st.write("Data Sample:")
        st.write(df.head())
    else:
        st.write("Please upload a CSV file.")

elif Employees_Overview_button:
    st.write("Employees Overview")
elif departments_button:
    st.write("Departments")
elif Salary_Analysis_button:
    st.write("Salary Analysis")
elif hiring_and_termination_button:
    st.write("Hiring and Termination")
elif Training_button:
    st.write("Training")
elif setting_button:
    st.write("Setting")
elif more_feature_button:
    st.write("More Feature")
