import streamlit as st
import pandas as pd

# Define function to display the column
def display_duplicate_column(df):
    columns_list = df.columns.tolist()
    df["IsDuplicate"] = df.duplicated(subset=columns_list, keep=False)
    df['Duplicate/Non Duplicate'] = df['IsDuplicate'].map({True: "Duplicate", False: "Non Duplicate"})
    return df

# Streamlit app
def main():
    st.title('Display Duplicate/Non Duplicate Column')

    # File uploader widget for Excel files
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the uploaded Excel file
        df = pd.read_excel(uploaded_file)
        # Display DataFrame
        st.write('Original DataFrame:')
        st.write(df)

        # Button to display the column
        if st.button('Display Duplicate/Non Duplicate Column'):
            df_with_duplicates = display_duplicate_column(df)
            st.write('DataFrame with Duplicate/Non Duplicate Column:')
            st.write(df_with_duplicates)

if __name__ == "__main__":
    main()
