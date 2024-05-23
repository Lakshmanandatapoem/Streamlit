import streamlit as st
import pandas as pd
import io
import sys 
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Information','Marketing Calculation','Sale Calculation'], 
        icons=['house', 'link', 'file-text','rocket'], menu_icon="cast", default_index=0)

if selected == "Information":
    st.subheader("Conversion Rate")
    st.write("""The conversion rate is a metric used to measure the effectiveness of marketing efforts, websites, or any other channels aimed at encouraging user actions. It's calculated as the percentage of users who complete a desired action out of the total number of users.\n
    Conversion Rate = ( Number of Conversions/Total Number of Visitors) × 100""")    

if selected == "Marketing Calculation":
    st.subheader("Conversion Rate(CR)")
    st.write("""The conversion rate is a metric used to measure the effectiveness of marketing efforts, websites, or any other channels aimed at encouraging user actions. It's calculated as the percentage of users who complete a desired action out of the total number of users.\n
    Conversion Rate = (Number of Conversions / Total Number of Visitors) × 100""")
    
    # Input fields for number of conversions and total number of visitors
    conversions = st.number_input('Enter the number of conversions:', min_value=0)
    visitors = st.number_input('Enter the total number of visitors:', min_value=0)
    st.write("conversions > visitors")
    
    # Button to calculate conversion rate
    if st.button('Calculate Conversion Rate'):
        if visitors > 0:
            conversion_rate = (conversions / visitors) * 100
            st.write(f'Conversion Rate: {conversion_rate:.2f}%')
        else:
            st.write('Please enter a valid numbers for visitors and conversions.')
    st.divider()

    st.subheader("Click Through Rate(CTR)")
    st.write("""Click Through Rate (CTR) is a key metric in digital marketing and online advertising that measures the effectiveness of a campaign by indicating the percentage of people who click on a specific link out of the total number of people who view the link (impressions).\n
    CTR=(Number of Clicks/Number of Impressions)×100""")
    # Input fields for number of conversions and total number of visitors
    Clicks = st.number_input('Enter the number of Clicks:', min_value=0)
    Impressions = st.number_input('Enter the total number of Impressions:', min_value=0)
    st.write("Impressions > Clicks")
    # Button to calculate conversion rate
    if st.button('Calculate Click Through Rate'):
        if Impressions > 0:
            Click_Thourgh_rate = (Clicks / Impressions) * 100
            st.write(f'Click_Thourgh_rate: {Click_Thourgh_rate:.2f}%')
        else:
            st.write('Please enter a valid numbers for Clicks and Impressions.')
    st.divider()


    st.subheader("Cost Per Click(CPC)")
    st.write("""Cost Per Click (CPC) is a metric used in online advertising to measure the cost incurred by an advertiser each time a user clicks on one of their ads. It is an essential metric for managing and optimizing advertising budgets..\n
    CPC = Total Cost/Total Number of Clicks""")
    # Input fields for number of conversions and total number of visitors
    Total_Cost = st.number_input('Enter the Total Cost:', min_value=0)
    Total_Number_Clicks = st.number_input('Enter the Total Number of Click:', min_value=0)
    # Button to calculate conversion rate
    if st.button('Calculate Cost Per Click(CPC)'):
        if Total_Number_Clicks > 0:
            Cost_Per_Click = (Total_Cost / Total_Number_Clicks)
            st.write(f'Cost_Per_Click: {Cost_Per_Click:.2f}%')
        else:
            st.write('Please enter a valid numbers for Cost and Click.')
    st.divider()