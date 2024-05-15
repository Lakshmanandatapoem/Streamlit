import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Title of the web app
    st.title("Excel File Reader and Analyzer")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the Excel file
        try:
            df = pd.read_excel(uploaded_file)

            # Display the dataframe
            st.write("Dataframe:")
            st.write(df)

            # Dropdown to select filter criteria
            filter_criteria = st.selectbox("Select Filter Criteria", ["Country", "State", "Region", "Category", "Sub-Category"])

            # Dropdown to select filter value
            filter_value = st.selectbox(f"Select {filter_criteria}", df[filter_criteria].unique())

            # Filtered dataframe
            filtered_df = df[df[filter_criteria] == filter_value]

            # Display Pivot Table
            st.write("Pivot Table:")
            pivot_table = pd.pivot_table(filtered_df, index='State', values=['Sales', 'Profit'], aggfunc='sum')
            st.write(pivot_table)

            # Plot
            st.write("Plot:")
            fig, ax = plt.subplots()
            pivot_table.plot(kind='bar', ax=ax)
            plt.xlabel('State')
            plt.ylabel('Amount')
            plt.title('Sales and Profit by State')
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
