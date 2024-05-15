import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Define the password
PASSWORD = "!@#123"

# Function to authenticate users
def authenticate(password):
    return password == PASSWORD

# Function to get data from Excel with caching
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

# Function to display login button
def login_button():
    password = st.text_input("Enter Password", type="password")
    if st.button("Login") and authenticate(password):
        return True
    return False

# Authenticate users
if not login_button():
    st.error("Access Denied! Incorrect password.")
    st.stop()

# Get data
df = get_data_from_excel()

# If login is successful, display the dashboard
st.title(":bar_chart: Sample Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df["Total"].sum())
average_rating = round(df["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [LINE CHART]
sales_by_Branch = df.groupby(by=["Branch"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.line(
    sales_by_Branch,
    x=sales_by_Branch.index,
    y="Total",
    title="<b>Sales by Branch</b>",
    color_discrete_sequence=["#0083B8"],  # Optional: Set color
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),  # Optional: Customize x-axis
    yaxis=dict(showgrid=False),  # Optional: Customize y-axis
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .sidebar .sidebar-content {visibility: hidden;}
            </style>
            """
# Show/hide sidebar based on checkbox state
if st.sidebar.checkbox("Show Sidebar", True):
    st.markdown(hide_st_style, unsafe_allow_html=True)
