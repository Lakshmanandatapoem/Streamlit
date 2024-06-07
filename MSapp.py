import streamlit as st
import pandas as pd
import io
import sys 
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Information','Marketing Calculation','Sale Calculation'], 
        icons=['house', 'link', 'file-text','rocket'], menu_icon="cast", default_index=0)

if selected == "Marketing Calculation":
    st.header("Marketing Calculation")
    option = st.selectbox(
        "Select the marketing metric to calculate:",
        ("Conversion Rate (CR)", "Click Through Rate (CTR)", "Cost Per Click (CPC)","Cost per Action (CPA)","Cost per Lead (CPL)","Customer Acquisition Cost (CAC)")
    )

    # Display the selected option
    st.write("You selected:", option)

    if option == "Conversion Rate (CR)":
        st.subheader("Conversion Rate (CR)")
        st.write("""The conversion rate is a metric used to measure the effectiveness of marketing efforts, websites, or any other channels aimed at encouraging user actions. It's calculated as the percentage of users who complete a desired action out of the total number of users.\n
        Conversion Rate = (Number of Conversions / Total Number of Visitors) × 100""")
        
        # Input fields for number of conversions and total number of visitors
        conversions = st.number_input('Enter the number of conversions:', min_value=0)
        visitors = st.number_input('Enter the total number of visitors:', min_value=0)
        
        # Button to calculate conversion rate
        if st.button('Calculate Conversion Rate'):
            if visitors > 0:
                conversion_rate = (conversions / visitors) * 100
                st.write(f'Conversion Rate: {conversion_rate:.2f}%')
            else:
                st.write('Please enter a valid number of visitors and conversions.')
    
    elif option == "Click Through Rate (CTR)":
        st.subheader("Click Through Rate (CTR)")
        st.write("""Click Through Rate (CTR) is a key metric in digital marketing and online advertising that measures the effectiveness of a campaign by indicating the percentage of people who click on a specific link out of the total number of people who view the link (impressions).\n
        CTR = (Number of Clicks / Number of Impressions) × 100""")
        
        # Input fields for number of clicks and total number of impressions
        clicks = st.number_input('Enter the number of clicks:', min_value=0)
        impressions = st.number_input('Enter the total number of impressions:', min_value=0)
        
        # Button to calculate click through rate
        if st.button('Calculate Click Through Rate'):
            if impressions > 0:
                click_through_rate = (clicks / impressions) * 100
                st.write(f'Click Through Rate: {click_through_rate:.2f}%')
            else:
                st.write('Please enter a valid number of clicks and impressions.')
    
    elif option == "Cost Per Click (CPC)":
        st.subheader("Cost Per Click (CPC)")
        st.write("""Cost Per Click (CPC) is a metric used in online advertising to measure the cost incurred by an advertiser each time a user clicks on one of their ads. It is an essential metric for managing and optimizing advertising budgets.\n
        CPC = Total Cost / Total Number of Clicks""")
        
        # Input fields for total cost and total number of clicks
        total_cost = st.number_input('Enter the total cost:', min_value=0)
        total_number_clicks = st.number_input('Enter the total number of clicks:', min_value=0)
        
        # Button to calculate cost per click
        if st.button('Calculate Cost Per Click (CPC)'):
            if total_number_clicks > 0:
                cost_per_click = (total_cost / total_number_clicks)
                st.write(f'Cost Per Click: {cost_per_click:.2f}')
            else:
                st.write('Please enter a valid number of total cost and clicks.')

    elif option == "Cost per Action (CPA)":
        st.subheader("Cost per Action (CPA)")
        st.write(""""Cost per Action (CPA) is a digital marketing metric that measures the cost associated with a specific action taken by a user as a result of an advertisement"\n
        CPA = Number of Actions / Total Cost""")

        # Input fields for total cost and total number of clicks
        total_Actions = st.number_input('Enter the total Actions:', min_value=0)
        total_cost = st.number_input('Enter the total Cost:', min_value=0)
        # Button to calculate cost per click
        if st.button('Calculate Cost Per Action (CPA)'):
            if total_Actions > 0:
                cost_per_Action = (total_cost / total_Actions)
                st.write(f'Cost Per Action: {cost_per_Action:.2f}')
            else:
                st.write('Please enter a valid number of total cost and Actions.')

    elif option == "Cost per Lead (CPL)":
        st.subheader("Cost Per Lead (CPL)")
        st.write(""""Cost per lead (CPL) is a metric used in marketing and advertising to measure the cost-effectiveness of a campaign in generating leads. It's calculated by dividing the total cost of the campaign by the number of leads generated"\n
        CPL = Total Campaign Cost / Number of Leads Generated""")

        # Input fields for total cost and total number of clicks
        Total_Campaign_Cost = st.number_input('Enter the Total_Campaing_Cost:', min_value=0)
        Number_of_Leads_Generated = st.number_input('Enter the Number_of_Leads_Generated:', min_value=0)
        # Button to calculate cost per click
        if st.button('Calculate Cost Per Lead (CPL)'):
            if Total_Campaign_Cost > 0:
                Cost_Per_Lead = (Total_Campaign_Cost / Number_of_Leads_Generated)
                st.write(f'Cost Per Lead: {Cost_Per_Lead:.2f}')
            else:
                st.write('Please enter a valid number of total campaign Cost and Leads.')

    elif option == "Customer Acquisition Cost (CAC)":
        st.subheader("Customer Acquisition Cost (CAC)")
        st.write(""""Customer Acquisition Cost (CAC) is a metric that measures the cost associated with acquiring a new customer. It is a crucial indicator for businesses to understand the efficiency of their marketing and sales efforts"\n
        CAC = Number of New Customers Acquired/Total Sales and Marketing Expenses""")

        # Input fields for total cost and total number of clicks
        New_Customers_Acquired = st.number_input('Enter the Number of New Customers Acquired:', min_value=0)
        Total_Sales_and_Marketing_Expenses = st.number_input('Enter the Total Sales and Marketing Expenses:', min_value=0)
        # Button to calculate cost per click
        if st.button('Customer Acquisition Cost (CAC)'):
            if New_Customers_Acquired > 0:
                Customer_Acquisition_Cost = (New_Customers_Acquired / Total_Sales_and_Marketing_Expenses)
                st.write(f'Cost Per Lead: {Customer_Acquisition_Cost:.2f}')
            else:
                st.write('Please enter a valid number New Customers Auquired and Sales,Mareketing Expenses.')
