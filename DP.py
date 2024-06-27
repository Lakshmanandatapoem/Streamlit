import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time
import io
import os
import sys
import subprocess
import sys 
import json
from io import BytesIO

st.set_page_config(
    page_title="Datapoem.Datateam",
    page_icon="https://green.datapoem.ai/img/datapoem-logo-white.d3e98fcd.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS for the option menu and background image
custom_css = f"""
<style>
/* Set the background image */
body {{
    background-image: url('https://datapoem.ai/img/gradient-color-bg.e99d22ef.svg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Increase the font size and padding of the option menu items */
.css-qrbaxs a {{
    font-size: 20px !important;
    padding: 10px 20px !important;
}}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)


# Create a container for the title and the menu
with st.container():
    selected = option_menu(
        menu_title="",
        options=["Home", "Paid Media", "Non Paid Media", "Competition","Nielsen", "Playground", "DMS", "QC", 'Setting', "More Feature"],
        icons=["house", "file-ppt", "journals",'journal-richtext' ,"database-fill-exclamation", "graph-up-arrow", "layout-text-sidebar-reverse", "search", "gear", "filter"],  # Provide an empty string for each option if no icons are used
        menu_icon="cast",
        default_index=0,  # Corrected to an integer
        orientation="horizontal",
    )
def login(username, password):
    # This function should be defined to handle login logic
    # For demonstration purposes, let's assume it always returns True
    return True
st.divider()
# Display content based on the selected option
if selected == "Home":
    if selected == "Home":
        # Add login form
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if login(username, password):
                st.success("Login successful!")
                # Place additional code here for what happens after successful login
            else:
                st.error("Login failed. Please check your username and password.")    
elif selected == "Paid Media":
        # Function to initialize session state
    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}

    # Function to save uploaded file
    def save_uploaded_file(uploaded_file):
        if not os.path.exists("tempDir"):
            os.makedirs("tempDir")
        file_path = os.path.join("tempDir", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    
    # Function to run the Python script
    def run_script(script_path):
        try:
            result = subprocess.run(['python', script_path], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Script ran successfully!")
                st.text(result.stdout)
            else:
                st.error("Error running the script.")
                st.error(result.stderr)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Streamlit app
    st.title("Python Script Runner")
    
    uploaded_file = st.file_uploader("Upload your Python script", type=["py"])
    
    if uploaded_file is not None:
        script_path = save_uploaded_file(uploaded_file)
        st.success(f"File saved successfully: {script_path}")
        
        if st.button("Run Script"):
            run_script(script_path)

    # Function to download Excel file
    def download_xlsx(df, label, filename):
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Function to download Excel file
    def download_csv(df, label, filename):
        csv_file = io.BytesIO()
        df.to_excel(csv_file, index=False)
        csv_file.seek(0)
        st.download_button(label=label, data=csv_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Initialize session state
    initialize_session_state()

    with st.sidebar:
        selected = option_menu("Main Menu", ['Data Filtering','Data Cleaning','Null Value Check','Summary','Datapoem Format'],#'Data Quality Check'], 
            icons=['filter','link', 'file-text', 'lightning','rocket','shield'], menu_icon="cast", default_index=0)
    
    #1. Data Filtering:    
    if selected == "Data Filtering":
        st.subheader("Data Filtering")
        uploaded_file = st.file_uploader("Upload a Python Script", type=["py"])
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file)
            if st.button('Run Script'):
                run_script(file_path)

    if selected == 'Data Cleaning':
        st.subheader("Data Cleaning Process")
        uploaded_files = st.file_uploader("Upload your excel file(s) for data cleaning process", type=["xlsx"], accept_multiple_files=True)

        # Check if files are uploaded
        if uploaded_files:
            # Loop through uploaded files
            for file in uploaded_files:
                # Read Excel file into a DataFrame
                df = pd.read_excel(file)
                # 1. Date Formatting
                #if 'Date' in df.columns:
                    #df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
                # 2. Remove empty rows
                df = df.dropna(how='all')
                # 3. Remove empty columns
                df = df.dropna(axis=1, how='all')
                # 4. Duplicate or Non-Duplicate Entry in Rows
                columns_list = df.columns.tolist()
                df["IsDuplicate"] = df.duplicated(subset=columns_list, keep=False)
                df['Duplicate/Non Duplicate'] = df['IsDuplicate'].map({True: "Duplicate", False: "Non Duplicate"})
                # 5. Convert Text format to numeric format
                if 'Impressions' in df.columns:
                    df['Impressions'] = pd.to_numeric(df['Impressions'])
                if 'GRPs' in df.columns:
                    df['GRPs'] = pd.to_numeric(df['GRPs'])
                if 'Media_Cost' in df.columns:
                    df['Media_Cost'] = pd.to_numeric(df['Media_Cost'])
                # 6. Blank metrics to Zero
                columns_to_replace = ['Impressions', 'Media_Cost', 'GRPs']
                df[columns_to_replace] = df[columns_to_replace].fillna(0).replace('', 0)
                # Store the modified DataFrame in the session state
                st.session_state.modified_files[file.name] = df
                def download_xlsx(df, label, filename):
                    if 'Raw' in filename:
                        filename = filename.replace('Raw', 'Processed')
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                # Display download button for the modified file
                download_xlsx(df, label=f'Download Modified File ({file.name})', filename=file.name)
                
            
        #2. Null Value Check Process:    
    if selected == 'Null Value Check':
            st.subheader("Null Values Checking Process")
            uploaded_files = st.file_uploader("Upload your excel file for null values checking process", type=["xlsx"], accept_multiple_files=True)
            if uploaded_files:
                dfs_to_save = []
                for file in uploaded_files:
                    df = pd.read_excel(file)
                    df['Month'] = df['Date'].apply(lambda x: x.month)
                    df['Year'] = df['Date'].apply(lambda x: x.year)
                        
                    null_cost = df
                    null_imp = df 
                    digtal_cost = null_cost[(null_cost['Master_Channel'] =='Digital') | (null_cost['Master_Channel'] =='Commerce & Search') | (null_cost['Master_Channel'] =='OOH') | (null_cost['Master_Channel'] =='DOOH')]
                    tv_cost = null_cost[(null_cost['Master_Channel'] =='TV') | (null_cost['Master_Channel'] =='Radio') | (null_cost['Master_Channel'] =='Print')| (null_cost['Master_Channel'] =='Cinema')]
                    digtal_imp = null_imp[(null_imp['Master_Channel'] =='Digital') | (null_imp['Master_Channel'] =='Commerce & Search') | (null_imp['Master_Channel'] =='OOH') | (null_imp['Master_Channel'] =='DOOH')]
                    tv_grp = null_imp[(null_imp['Master_Channel'] =='TV') | (null_imp['Master_Channel'] =='Radio') | (null_imp['Master_Channel'] =='Print') | (null_imp['Master_Channel'] =='Cinema')  ]
                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_cost.groupby(col)["Impressions"].sum()
                    

                    #1. Null Media_Cost - Digital,Commerce & Search

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_cost_group = digtal_cost.groupby(col)[['Impressions', 'Media_Cost']].sum()
                    digtal_cost_group = digtal_cost_group[digtal_cost_group['Impressions']>10000]
                    digtal_cost_group = digtal_cost_group[digtal_cost_group['Media_Cost']== 0]
                    dfs_to_save.append((digtal_cost.reset_index(), 'Digital Cost Raw'))
                    dfs_to_save.append((digtal_cost_group.reset_index(), 'Digital Cost Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_cost_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(digtal_cost_group.reset_index(), label=f'Digtal Cost Null Summary File ({file.name})', filename=file.name)
                    digtal_cost['tuple'] = digtal_cost[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_cost
                    # Display download button for the modified file with unique key
                    download_xlsx_2(digtal_cost[digtal_cost['tuple'].isin(digtal_cost_group.index)], label=f'Digtal Cost Null Raw File ({file.name})', filename=file.name)

                    #2. Null Impressions - Digital,Commerce & Search

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Package_Placement_Name']
                    digtal_imp_group = digtal_imp.groupby(col)[['Impressions', 'Media_Cost']].sum()
                    digtal_imp_group = digtal_imp_group[digtal_imp_group['Media_Cost']>1000]
                    digtal_imp_group = digtal_imp_group[digtal_imp_group['Impressions']==0]
                    dfs_to_save.append((digtal_imp.reset_index(), 'Digital Imp Raw'))
                    dfs_to_save.append((digtal_imp_group.reset_index(), 'Digital Imp Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_imp_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(digtal_imp_group.reset_index(), label=f'Digtal Imp Null Summary File ({file.name})', filename=file.name)
                    digtal_imp['tuple'] = digtal_imp[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = digtal_imp
                    # Display download button for the modified file with unique key
                    download_xlsx_2(digtal_imp[digtal_imp['tuple'].isin(digtal_imp_group.index)], label=f'Digtal Imp Null Raw File ({file.name})', filename=file.name)
                    
                    #3. Null GRPs - TV
                    
                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Daypart']
                    tv_grp_group = tv_grp.groupby(col)[['GRPs', 'Media_Cost']].sum()
                    tv_grp_group = tv_grp_group[tv_grp_group['Media_Cost']>50000]
                    tv_grp_group = tv_grp_group[tv_grp_group['GRPs']==0]
                    dfs_to_save.append((tv_grp.reset_index(), 'TV GRP Raw'))
                    dfs_to_save.append((tv_grp_group.reset_index(), 'TV GRP Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_grp_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(tv_grp_group.reset_index(), label=f'TV Null GRPs Summary File ({file.name})', filename=file.name)
                    tv_grp['tuple'] = tv_grp[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_grp
                    # Display download button for the modified file with unique key
                    download_xlsx_2(tv_grp[tv_grp['tuple'].isin(tv_grp_group.index)], label=f'TV Null GRPs Raw File ({file.name})', filename=file.name)
                    
                    #4. Null Media_Cost - TV

                    col = ['Year','Month','Master_Channel','Channel','Raw_Partner','Audience','Daypart']
                    tv_cost_group = tv_cost.groupby(col)[['GRPs', 'Media_Cost']].sum()
                    tv_cost_group = tv_cost_group[tv_cost_group['GRPs']>1]
                    tv_cost_group = tv_cost_group[tv_cost_group['Media_Cost']== 0]
                    dfs_to_save.append((tv_cost.reset_index(), 'TV Cost Raw'))
                    dfs_to_save.append((tv_cost_group.reset_index(), 'TV Cost Summary'))

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_cost_group
                    # Function to download Excel file
                    def download_xlsx_2(df, label, filename):
                    # Create a BytesIO object to store the Excel file
                        excel_file = io.BytesIO()
                    # Write the DataFrame to the BytesIO object
                        df.to_excel(excel_file, index=False)
                    # Set the cursor to the beginning of the BytesIO object
                        excel_file.seek(0)
                    # Set up download button
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    # Display download button for the modified file
                    download_xlsx_2(tv_cost_group.reset_index(), label=f'TV Null Cost Summary File ({file.name})', filename=file.name)
                    tv_cost['tuple'] = tv_cost[col].apply(lambda x: tuple(x),axis=1)
                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = tv_cost
                    # Display download button for the modified file with unique key
                    download_xlsx_2(tv_cost[tv_cost['tuple'].isin(tv_cost_group.index)], label=f'TV Null Cost Raw File ({file.name})', filename=file.name)
                            # Create an in-memory bytes buffer to hold the Excel file content
                    output = io.BytesIO()
                    
                    # # Create a Pandas Excel writer using XlsxWriter engine
                    # with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    #     # Write each DataFrame to a separate sheet in the Excel file
                    #     for df, label in dfs_to_save:
                    #         df.to_excel(writer, sheet_name=label, index=False)
                    
                    # # Set the cursor to the beginning of the BytesIO object
                    # output.seek(0)
                    
                    # # Display download button for the Excel file
                    # st.download_button(label='Download Excel File', data=output.getvalue(), file_name='null_value_check_results.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    break
     
        # Check if "Summary" is selected
    if selected == 'Summary':
            st.subheader("Summary Preparation Process")
            option = st.selectbox(
                "Select the brand to prepare the summary",
                ("Dove PW", "Dove Deo", "DMC PW", "DMC Deo", "Degree Deo", "Axe Deo", "Dove MB + Superbowl", "Dove Cross", "Degree Cross", "Axe Cross","DMC Cross")
            )
            st.write("selected:", option)
            
            # Set the size of the dropdown menu
            st.markdown(
                "<style>.css-1a7xih0{font-size: small !important;}</style>", 
                unsafe_allow_html=True
            )
        #Axe Cross Cateogry Summary:
            if option == 'Axe Cross':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                        excel_file = io.BytesIO()
                        df.to_excel(excel_file, index=False)
                        excel_file.seek(0)
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)    
                if uploaded_files:
                        for file in uploaded_files:
                            Axe_Cross = pd.read_excel(file)
                            Axe_Cross['Date'] = pd.to_datetime(Axe_Cross['Date'])
                            Axe_Cross = Axe_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost', 'Video_Views']
                            Axe_Cross[numeric_columns] = Axe_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Axe_Cross_pivot_table = Axe_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Axe_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            #download_xlsx(Axe_Cross, label='Download Modified File (Mapped)', filename="Axe Cross Category Mapped Raw.xlsx")
                            download_xlsx(Axe_Cross_pivot_table, label='Download Modified File (Summary)', filename="Axe Cross Category Summary.xlsx")
        #Degree Cross Cateogry Summary:
            if option == 'Degree Cross':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:    
                        for file in uploaded_files:
                            Degree_Cross = pd.read_excel(file)
                            Degree_Cross['Date'] = pd.to_datetime(Degree_Cross['Date'])
                            Degree_Cross = Degree_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            Degree_Cross[numeric_columns] = Degree_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Degree_Cross_pivot_table = Degree_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Degree_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            #download_xlsx(Degree_Cross, label='Download Modified File (Mapped)', filename="Degree Cross Category Mapped Raw.xlsx")
                            download_xlsx(Degree_Cross_pivot_table, label='Download Modified File (Summary)', filename="Degree Cross Category Summary.xlsx")
        #DMC Cross Cateogry Summary:
            if option == 'DMC Cross':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:
                    
                        for file in uploaded_files:
                            DMC_Cross = pd.read_excel(file)
                            DMC_Cross['Date'] = pd.to_datetime(DMC_Cross['Date'])
                            DMC_Cross = DMC_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            DMC_Cross[numeric_columns] = DMC_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            DMC_Cross_pivot_table = DMC_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[DMC_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            #download_xlsx(DMC_Cross, label='Download Modified File (Mapped)', filename="DMC Cross Category Mapped Raw.xlsx")
                            download_xlsx(DMC_Cross_pivot_table, label='Download Modified File (Summary)', filename="DMC Cross Category Summary.xlsx")
        #Dove Cross Cateogry Summary:
            if option == 'Dove Cross':
            # Function to download Excel file
                def download_xlsx(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                if uploaded_files:
                    
                        for file in uploaded_files:
                            Dove_Cross = pd.read_excel(file)
                            Dove_Cross['Date'] = pd.to_datetime(Dove_Cross['Date'])
                            Dove_Cross = Dove_Cross.fillna(0)
                            numeric_columns = ['Impressions', 'Clicks', 'Media_Cost']
                            Dove_Cross[numeric_columns] = Dove_Cross[numeric_columns].apply(pd.to_numeric, errors='coerce')
                            Dove_Cross_pivot_table = Dove_Cross.pivot_table(
                                values=['Impressions', 'Clicks', 'Media_Cost'], 
                                index=[Dove_Cross['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience'],
                                aggfunc='sum').reset_index()
                            #download_xlsx(DMC_Cross, label='Download Modified File (Mapped)', filename="DMC Cross Category Mapped Raw.xlsx")
                            download_xlsx(Dove_Cross_pivot_table, label='Download Modified File (Summary)', filename="Dove Cross Category Summary.xlsx")

        # Dove + Superbowl Cateogry Summary:
            if option == 'Dove MB + Superbowl':
               # Function to download the Excel file
                def download_xlsx_Dove_Superbowl(df, label, filename):
                            excel_file = io.BytesIO()
                            df.to_excel(excel_file, index=False)
                            excel_file.seek(0)
                            st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                Dove_MB_Superbowl_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                dataframes = []
                if Dove_MB_Superbowl_files:                            
                    for file in Dove_MB_Superbowl_files:
                            df = pd.read_excel(file)
                            dataframes.append(df)
                   # Concatenate all DataFrames into a single DataFrame
                    Dove_MB_Superbowl_files_df = pd.concat(dataframes, ignore_index=True)
                    st.write("Dove MB + Superbowl Raw Data")
                    # Display the concatenated DataFrame
                    st.write(Dove_MB_Superbowl_files_df)
                    # Streamlit file uploader for the Campaign Mapping file
                campaign_mapping_file = st.file_uploader("Upload your Campaign Mapping file", type=["xlsx"], accept_multiple_files=False)             
                if campaign_mapping_file is not None:
                                        # Read the Excel file
                            campaign_mapping_file_df = pd.read_excel(campaign_mapping_file)
                            # Rename the column
                            campaign_mapping_file_df.rename(columns={'Prisma Campaign Name': 'Prisma_Campaign_Secondary'}, inplace=True)
                            # Display the DataFrame with the renamed column
                            st.write("Dove MB + Superbowl Campaign Mapping File")
                            st.write(campaign_mapping_file_df)
                 # Merge the Campaign Mapping DataFrame with the Dove MB Superbowl DataFrame
                Dove_MB_merged_final = Dove_MB_Superbowl_files_df.merge(campaign_mapping_file_df[['Prisma_Campaign_Secondary','Superbowl']], on='Prisma_Campaign_Secondary', how='left')
                Dove_MB_merged_final['Superbowl'] = Dove_MB_merged_final['Superbowl'].fillna('Dove Masterbrand Non Superbowl')
                st.write("Dove MB + Superbowl Mapped Data")
                st.write(Dove_MB_merged_final)
                # Convert 'Date' column to datetime and handle missing values
                Dove_MB_merged_final['Date'] = pd.to_datetime(Dove_MB_merged_final['Date'], errors='coerce')
                Dove_MB_merged_df = Dove_MB_merged_final.fillna(0)
                # Ensure specific columns are numeric
                numeric_columns = ['Impressions', 'Clicks', 'Media_Cost','GRPs']
                Dove_MB_merged_df[numeric_columns] = Dove_MB_merged_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
                # Create a pivot table with the required aggregations
                Dove_MB_Superbowl_pivot_table = Dove_MB_merged_df.pivot_table(
                    values=['Impressions', 'Clicks', 'Media_Cost','GRPs'],
                    index=[Dove_MB_merged_df['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience','Superbowl'],
                    aggfunc='sum').reset_index()
                # Download buttons for the processed files
                download_xlsx_Dove_Superbowl(Dove_MB_merged_df, label='Download Modified File (Mapped)', filename="Dove_MB_Superbowl_Mapped_Raw.xlsx")
                download_xlsx_Dove_Superbowl(Dove_MB_Superbowl_pivot_table, label='Download Modified File (Summary)', filename="Dove_MB_Superbowl_Summary.xlsx")          # Read each file into a DataFrame               
                                
  
        #Dove PW Summary:

            if option == 'Dove PW':
                # Function to download Excel file
                def download_xlsx_Dove_PW(df, label, filename):
                    excel_file = io.BytesIO()
                    df.to_excel(excel_file, index=False)
                    excel_file.seek(0)
                    st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                # File uploader for Dove PW files
                Dove_PW_files = st.file_uploader("Upload your Excel file to prepare the Summary", type=["xlsx"], accept_multiple_files=True)
                dataframes = []
                if Dove_PW_files:
                    for file in Dove_PW_files:
                        df = pd.read_excel(file)
                        dataframes.append(df)
                    Dove_PW_files_df = pd.concat(dataframes, ignore_index=True)
                    
                    # Concatenate columns to create 'Audience_mapping_df' column
                    Dove_PW_files_df['Audience_mapping_df'] = Dove_PW_files_df[['Channel', 'Raw_Partner', 'Audience']].astype(str).agg('-'.join, axis=1)
                    
                    st.write("Dove PW Raw Data")
                    st.write(Dove_PW_files_df)

                # File uploader for Campaign Mapping file
                mapping = st.file_uploader("Upload your Campaign Mapping file", type=["xlsx"], accept_multiple_files=False)
                if mapping is not None:
                    try:
                        # Automatically select the "daypart" sheet
                        daypart_df = pd.read_excel(mapping, sheet_name='Daypart')
                        st.write("Daypart Mapping File - Sheet: daypart")
                        st.write(daypart_df)
                        
                        # Automatically select the "UE" sheet for Audience
                        UE_df = pd.read_excel(mapping, sheet_name='UE')
                        st.write("Universal Estimate Mapping File - Sheet: UE")
                        st.write(UE_df)

                        # Automatically select the "Campaign" sheet for Audience
                        Campaign_df = pd.read_excel(mapping, sheet_name='Dove PW C')
                        st.write("Campaign Mapping File - Sheet: Dove PW C")
                        st.write(Campaign_df)

                        # Automatically select the "Audience" sheet
                        audience_df = pd.read_excel(mapping, sheet_name='Dove PW A')
                        st.write("Audience Mapping File - Sheet: Dove PW A")
                        st.write(audience_df)
                        audience_df['Audience_mapping_df'] = audience_df[['Channel', 'Raw_Partner', 'Audience']].astype(str).agg('-'.join, axis=1)
                        
                    except ValueError as e:
                        st.error(f"Error reading sheets from the mapping file: {e}")
                    
                    # Check if 'Daypart' columns are present
                    if 'Daypart' in Dove_PW_files_df.columns and 'Daypart' in daypart_df.columns:
                        # Merge Dove PW DataFrame with daypart DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(daypart_df, on='Daypart', how='left')
                    else:
                        st.error("Daypart column not found in either the Dove PW data or the Daypart mapping data.")

                    # Check if 'Audience' columns are present
                    if 'Audience' in Dove_PW_files_df.columns and 'Audience' in UE_df.columns:
                        # Merge the resulting DataFrame with audience DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(UE_df, on='Audience', how='left')
                    else:
                        st.error("Audience column not found in either the Dove PW data or the Audience mapping data.")
                    
                    # Check if 'Campaign' columns are present
                    if 'Campaign' in Dove_PW_files_df.columns and 'Campaign' in Campaign_df.columns:
                        # Merge the resulting DataFrame with Campaign DataFrame
                        Dove_PW_files_df = Dove_PW_files_df.merge(Campaign_df, on='Campaign', how='left')
                    else:
                        st.error("Campaign column not found in either the Dove PW data or the Campaign mapping data.")
                    
                    # Check if 'Audience_mapping_df' column is present in both DataFrames
                    if 'Audience_mapping_df' in Dove_PW_files_df.columns and 'Audience_mapping_df' in audience_df.columns:
                        # Merge Dove PW DataFrame with audience DataFrame on 'Audience_mapping_df'
                        Dove_PW_files_df = Dove_PW_files_df.merge(audience_df, on='Audience_mapping_df', how='left')
                    else:
                        st.error("Audience_mapping_df column not found in either the Dove PW data or the Audience mapping data.")
                    
                    # Drop unwanted columns
                    columns_to_drop = ['Audience_mapping_df', 'Channel_y', 'Raw_Partner_y', 'Audience_y']
                    Dove_PW_files_df = Dove_PW_files_df.drop(columns=columns_to_drop, errors='ignore')
                    Dove_PW_files_df = Dove_PW_files_df.rename(columns={
                        'Channel_x': 'Channel',
                        'Raw_Partner_x': 'Raw_Partner',
                        'Audience_x': 'Audience'
                    })
                    
                    

                    # Ensure the Date column is in datetime format
                    Dove_PW_files_df['Date'] = pd.to_datetime(Dove_PW_files_df['Date'], errors='coerce')
                    
                    # Check for non-null and properly formatted Date values
                    if Dove_PW_files_df['Date'].isnull().any():
                        st.error("There are null or improperly formatted Date values in the data.")
                    # Display the mapped data
                    st.write("Mapped Dove PW Data")
                    st.write(Dove_PW_files_df)
                    
                    # Creating pivot table
                    Dove_PW_pivot_table_77 = Dove_PW_files_df.pivot_table(
                        values=['Impressions', 'Clicks', 'Media_Cost', 'GRPs', 'Video_Views'],
                        index=[Dove_PW_files_df['Date'].dt.to_period('M'), 'Category', 'Brand', 'Master_Channel', 'Channel', 'Campaign', 'Hierarchy', 'Product Line', 'Prisma_Campaign_Secondary', 'Raw_Partner', 'Standardized_Partner', 'Audience', 'Mapped Audience', 'Daypart', 'Bucket', 'Mapped to OLD RROI Logic'],
                        aggfunc='sum'
                    ).reset_index()

                    # Provide download button for mapped data
                    download_xlsx_Dove_PW(Dove_PW_files_df, label="Download Mapped Dove PW Data", filename="Dove_PW_Processed_File.xlsx")
                    download_xlsx_Dove_PW(Dove_PW_pivot_table_77, label='Download Modified File (Summary)', filename="Dove_PW_Summary.xlsx")

                    # Display the pivot table for verification
                    st.write("Pivot Table Summary")
                    st.write(Dove_PW_pivot_table_77)
    if selected == "Datapoem Format":
            st.header("Datapoem Format Preparation Process")
            uploaded_files = st.file_uploader("Upload your Excel file(s) to prepare the datapoem format:", type=["xlsx"], accept_multiple_files=True)
            if uploaded_files is not None:
                for file in uploaded_files:
                    # Read each uploaded file as a DataFrame
                    df = pd.read_excel(file)
                    # Rename the columns
                    df.rename(columns={'Channel': 'Channel Name','Brand':'Brand Name','Master_Channel':'Master Channel','Product_Line':'Product Line','Package_Placement_Name':'Placement Name','Campaign':'Campaign Name','Prisma_Campaign_Secondary':'Merged Campaign name','Raw_Partner':'Platform','Standardized_Partner':'Merged Platform','Media_Cost':'Spends','Mapped Audience':'Merged Audience'}, inplace=True)
                    
                    raw_format = [
                        'HH Universe','Year', 'Month', 'Day','Start Date', 'End Date', 'Number of Days', 
                        'Sub category', 'Business Unit','Model Name', 'Brand or Competition', 'Modeling Brand',
                        'Advertiser', 'Sub Brand', 'Media type', 'Campaign Objective',
                        'Media Channel', 'Merged Media Channel',
                        'Merged TV Channel Name',  'Platform Genre',
                        'Merged Platform Genre', 'Vendor Name', 'Influencer Name', 'Live Cricket or other live events or Not live',
                        'Event Type', 'Language', 'Merged Language', 'Ad Type', 'Merged Ad Type',
                        'Country', 'Market/State','Merged Market/State', 'City', 'Merged City', 'Modeling Market', 'Demographic',
                        'Sessions',  'Leads', 'Engagement', 'Clicks', 'Key Words', 'DOBR Quotes',
                        'Overall Quotes', 'Modeling Metrics (Data POEM will fill in)', 'Likes', 'Shares', 'Engagements', 'SMS',
                        'Push Notification', 'Email', 'App Installs', 'Search Volume', 'Offer Details', 'Coupons', 'Orders', 'Revenue',
                        'BC DEPARTMENT', 'BC SUPER CATEGORY', 'BC CATEGORY', 'BC SUB CATEGORY', 'BRAND OWNER HIGH', 'BRAND FAMILY',
                        'BRAND HIGH', 'BRAND LOW', 'BRAND OWNER LOW', '$', 'Units', 'Avg Unit Price', 'Any Promo Unit Price', 'No Promo Unit Price',
                        'Disp w/o Feat Unit Price', 'Feat w/o Disp Unit Price', 'Feat & Disp Unit Price', 'Any Disp Unit Price', 'Any Feat Unit Price',
                        'Any Price Decr Unit Price', 'TDP', '%ACV', 'Any Promo $', 'No Promo $']

                    DP_format_columns = pd.DataFrame(columns=raw_format)
                    DP_Format = pd.concat([df, DP_format_columns], axis=1)
                    DP_Format['Date'] = pd.to_datetime(DP_Format['Date'])
                    DP_Format['Year'] = DP_Format['Date'].dt.year
                    DP_Format['Month'] = DP_Format['Date'].dt.month
                    DP_Format['Day'] = DP_Format['Date'].dt.day
                    DP_Format['Date'] = DP_Format['Date'].dt.date             

                    # Store the modified DataFrame in the session state
                    st.session_state.modified_files[file.name] = DP_Format

                    def download_xlsx_4(df, label, filename):
                        excel_file = io.BytesIO()
                        df.to_excel(excel_file, index=False)
                        excel_file.seek(0)
                        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                    # Call the function to display download button for the modified file
                    download_xlsx_4(DP_Format, label=f'Download Modified File ({file.name})', filename=file.name)
          

elif selected == "Non Paid Media":
    st.subheader("Non Digital Coupon Calculation")
    
    # Text inputs for the user to input dates
    input_date_1_str = st.text_input("Enter the first date (dd-mm-yyyy)", "01-05-2024")
    input_date_2_str = st.text_input("Enter the second date (dd-mm-yyyy)", "31-05-2024")
    
    try:
        # Convert input dates to datetime objects
        input_date_1 = pd.to_datetime(input_date_1_str, format='%d-%m-%Y')
        input_date_2 = pd.to_datetime(input_date_2_str, format='%d-%m-%Y')
        days_between_inputs = (input_date_2 - input_date_1).days
        st.write(f"Number of days between {input_date_1.date()} and {input_date_2.date()} is: {days_between_inputs + 1} days")
    except ValueError:
        st.write("Please enter valid dates in the format dd-mm-yyyy.")
    
    # File uploader for non-digital coupon file
    uploaded_file = st.file_uploader("Choose a Non Digital Coupon File", type=['xlsx'])

    if uploaded_file is not None:
        # Read the uploaded Excel file
        df = pd.read_excel(uploaded_file)
        # Display some information More More Feature More Feature the uploaded file
        st.write("### Uploaded the Non Digital Coupon File:")
        st.write(df)

        # Ensure the date columns are in datetime format
        df['Issue_Date'] = pd.to_datetime(df['Issue_Date'], format='%Y-%m-%d')
        df['Expire_Date'] = pd.to_datetime(df['Expire_Date'], format='%Y-%m-%d')

        # Calculate the Expire_Date(DP) column
        df['Expire_Date(DP)'] = df.apply(
            lambda row: row['Issue_Date'] + pd.DateOffset(weeks=8) 
            if row['ConsumerRedemptionPeriod'] in [9, 10] 
            else row['Expire_Date'], 
            axis=1
        )

        # Calculate the number of overlapping days with the input date range
        def calculate_overlapping_days(row, start_date, end_date):
            if (start_date >= row['Issue_Date'] and end_date <= row['Expire_Date(DP)']) or (start_date < row['Expire_Date(DP)'] and end_date > row['Issue_Date']):
                return (min(row['Expire_Date(DP)'], end_date) - max(row['Issue_Date'], start_date)).days + 1
            else:
                return 0

        df['Date Range'] = df.apply(calculate_overlapping_days, axis=1, start_date=input_date_1, end_date=input_date_2)

        # Calculate the final cost
        df['Final Cost'] = df['WeeklyCost'] / 7 * df['Date Range']

        # Display the updated DataFrame with the new columns including Final Cost
        st.write("### Calculated Non Digital Coupon Data:")
        st.write(df)

        # Optionally, allow the user to download the updated DataFrame as an Excel file
        @st.cache_data
        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

        excel_data = convert_df_to_excel(df)

        st.download_button(
            label="Download updated file as Excel",
            data=excel_data,
            file_name="updated_coupon_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
elif selected == "Competition":
    st.subheader("Kantar")
    st.subheader("Pathmatics")
elif selected == "Nielsen":
        # Function to read text file and convert to DataFrame
    def convert_to_dataframe(uploaded_file):
        # Read the text file with '|' delimiter
        df = pd.read_csv(uploaded_file, delimiter='|', dtype={'UPC': 'object'})
        
        # Check if 'Period Description' column exists
        if 'Period Description' in df.columns:
            # Extract dates from 'Period Description' if the file name contains "prd"
            if 'prd' in uploaded_file.name.lower():
                df['Date'] = pd.to_datetime(df['Period Description'].str.extract(r'(\d{2}/\d{2}/\d{2})')[0], format='%m/%d/%y')
        return df

    # Function to download DataFrame as CSV file
    def download_csv_raw(df, label, filename='Nielsen_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")

    def download_csv_pc(df, label, filename='PC_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")
    def download_csv_BnW(df, label, filename='BnW_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")
    def download_csv_NIC(df, label, filename='NIC_Filtered_Raw_Data.csv'):
        # Create a StringIO object to store the CSV file
        output = io.StringIO()
        # Write the DataFrame to the StringIO object
        df.to_csv(output, index=False)
        # Set up the StringIO object for downloading
        csv_data = output.getvalue().encode('utf-8')
        st.download_button(label=label, data=csv_data, file_name=filename, mime="text/csv")       

    # Sidebar function for filtering data
    def sidebar_filters(data):
        
        st.sidebar.header("Filter by Market Description")
        MARKET_DESCRIPTION = st.sidebar.multiselect("Select the MARKET_DESCRIPTION:", options=data["Market Description"].unique())
        data = data[data["Market Description"].isin(MARKET_DESCRIPTION)]

        st.sidebar.header("Filter by Brand")
        BRAND = st.sidebar.multiselect("Select the Brand:", options=data["BRAND"].unique())
        data = data[data["BRAND"].isin(BRAND)]

        st.sidebar.header("Filter by Category")
        CATEGORY = st.sidebar.multiselect("Select the CATEGORY:", options=data["CATEGORY"].unique())
        data = data[data["CATEGORY"].isin(CATEGORY)]
        
        st.sidebar.header("Filter by SUB Category")
        SUB_CATEGORY = st.sidebar.multiselect("Select the SUB CATEGORY:", options=data["SUB CATEGORY"].unique())
        data = data[data["SUB CATEGORY"].isin(SUB_CATEGORY)]

        return data

    # Function to generate pivot table from filtered data
    def generate_pivot_table(filtered_data):
        pivot_table = filtered_data.pivot_table(index=['Market Description', 'BRAND','CATEGORY','SUB CATEGORY'], values='$', aggfunc='sum')
        pivot_table.reset_index(inplace=True)  # Reset index to include index columns in the DataFrame
        return pivot_table


    # Main function to run the Streamlit web application
    def main():
        # Set title and description
        st.subheader('Nielsen')
        # Upload text files
        uploaded_files = st.file_uploader("Choose Text files", type=['txt'], accept_multiple_files=True)

        uploaded_file_names = set()  # Set to store uploaded file names
        dfs = []  # List to store DataFrames
        file_rows = {}  # Dictionary to store number of rows for each file

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Check if the file is already uploaded
                if uploaded_file.name not in uploaded_file_names:
                    uploaded_file_names.add(uploaded_file.name)  # Add the file name to the set
                    # Read and convert each text file
                    df = convert_to_dataframe(uploaded_file)
                    dfs.append(df)  # Append the DataFrame to the list
                    file_rows[uploaded_file.name] = df.shape[0]  # Store the number of rows
                    file_name = uploaded_file.name  # Get the name of the uploaded file
                    # Display the file name and DataFrame
                    st.write(f"File Name: {file_name}")
                    st.write(df)
                else:
                    st.warning(f"File '{uploaded_file.name}' is already uploaded and cannot be browsed again.")

        # Merge DataFrames if multiple files are uploaded
        if len(dfs) > 0:
            Nielsen_Raw_Data = dfs[0]  # Initialize Nielsen_Raw_Data with the first DataFrame
            for df in dfs[1:]:
                # Adjust keys accordingly
                if 'Period Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Period Key'], how='left')
                if 'Market Key' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['Market Key'], how='left')
                if 'PRODUCT KEY' in df.columns:
                    Nielsen_Raw_Data = Nielsen_Raw_Data.merge(df, on=['PRODUCT KEY'], how='left')

            # Drop the 'Period Description' column
            # Nielsen_Raw_Data.drop(columns=['Period Description','Market Key','PRODUCT KEY','Period Key'], inplace=True)

            # Count rows for Nielsen_Raw_Data
            merged_rows = Nielsen_Raw_Data.shape[0]

            st.write("Nielsen Raw Data:")
            st.write(Nielsen_Raw_Data)
            st.write(f"Number of rows in Nielsen_Raw_Data: {merged_rows}")

            # Display number of rows for each file
            st.write("Number of rows in each uploaded file:")
            for file_name, num_rows in file_rows.items():
                st.write(f"{file_name}: {num_rows}")

            # Add download buttons for the Nielsen_Raw_Data
            download_csv_raw(Nielsen_Raw_Data, label="Download Raw_Data (csv)")
            
            #Bar:
                    
            Bar_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['CATEGORY'].isin(['SOAP'])]
            Bar_2 = Bar_1[Bar_1['SUB CATEGORY'].isin(['BAR'])]
            Bar_3 = Bar_2[Bar_2['Market Description'].isin(['Total US xAOC'])]
            Bar_4 = Bar_3[Bar_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Bar_5 = Bar_4[~Bar_4['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]

            #Bodywash

            Bodywash_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['CATEGORY'].isin(['BODY WASH','EXFOLIATOR/SCRUBS'])]
            Bodywash_2 = Bodywash_1[Bodywash_1['SUB CATEGORY'].isin(['CHILD','UNISEX','WOMEN'])]
            Bodywash_3 = Bodywash_2[Bodywash_2['Market Description'].isin(['Total US xAOC'])]
            Bodywash_4 = Bodywash_3[Bodywash_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Bodywash_5 = Bodywash_4[~Bodywash_4['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]

            #PW DMC

            PW_DMC_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            PW_DMC_2 = PW_DMC_1[PW_DMC_1['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            PW_DMC_3 = PW_DMC_2[PW_DMC_2['CATEGORY'].isin(['BODY WASH','EXFOLIATOR/SCRUBS','SOAP'])]

            ########################################### Deodorant ##########################################################

            #Deo DMC

            Deo_DMC_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_DMC_2 = Deo_DMC_1[Deo_DMC_1['BRAND FAMILY'].isin(['DOVE MEN + CARE (UNILEVER HOME & PERSONAL CARE)'])]
            Deo_DMC_3 = Deo_DMC_2[Deo_DMC_2['CATEGORY'].isin(['AP & DEO','DEODORANT'])]

            #Deo Dove

            Deo_Dove_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Dove_2 = Deo_Dove_1[Deo_Dove_1['CATEGORY'].isin(['AP & DEO','DEODORANT'])]
            Deo_Dove_3 = Deo_Dove_2[Deo_Dove_2['SUB CATEGORY'].isin(['WOMEN'])]
            Deo_Dove_4 = Deo_Dove_3[Deo_Dove_3['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]

            #Deo Axe

            Deo_Axe_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Axe_2 = Deo_Axe_1[Deo_Axe_1['CATEGORY'].isin(['AP & DEO','DEODORANT','BODY SPRAY'])]
            Deo_Axe_3 = Deo_Axe_2[Deo_Axe_2['BRAND'].isin(['AXE (UNILEVER HOME & PERSONAL CARE)'])]

            #Deo Degree

            Deo_Degree_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Deo_Degree_2 = Deo_Degree_1[Deo_Degree_1['BRAND'].isin(['DEGREE (UNILEVER HOME & PERSONAL CARE)',"UNLIMITED BY DEGREE (UNILEVER HOME & PERSONAL CARE)"])]
            Deo_Degree_3 = Deo_Degree_2[Deo_Degree_2['CATEGORY'].isin(['AP & DEO','DEODORANT'])]

            PC_Filted_Data = pd.concat([Bar_5, Bodywash_5, PW_DMC_3, Deo_DMC_3, Deo_Dove_4, Deo_Axe_3, Deo_Degree_3])     
            download_csv_pc(PC_Filted_Data, label="Download PC_Brands_Data (csv)")

            #Bnw Brands
            #Dove Haircare

            Dove_Haircare_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Dove_Haircare_2 = Dove_Haircare_1[Dove_Haircare_1['BRAND'].isin(['DOVE (UNILEVER HOME & PERSONAL CARE)'])]
            Dove_Haircare_3 = Dove_Haircare_2[Dove_Haircare_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','BODY','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY','REMAINING HBL'])]

            #Nexxus

            Nexxus_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Nexxus_2 = Nexxus_1[Nexxus_1['BRAND'].isin(['NEXXUS (NEXXUS PRODUCTS COMPANY)'])]
            Nexxus_3 = Nexxus_2[Nexxus_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY'])]

            #Sheamoisture

            sheamoisture_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            sheamoisture_2 = sheamoisture_1[sheamoisture_1['BRAND'].isin(['SHEA MOISTURE (SUNDIAL BRANDS LLC)'])]
            sheamoisture_3 = sheamoisture_2[sheamoisture_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','BODY','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY'])]

            #Tresemme

            Tresemme_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Tresemme_2 = Tresemme_1[Tresemme_1['BRAND'].isin(['SHEA MOISTURE (SUNDIAL BRANDS LLC)'])]
            Tresemme_3 = Tresemme_2[Tresemme_2['CATEGORY'].isin(['SHAMPOO','STYLING PRODUCTS','SHAMPOO AND CONDITIONER COMBO','CONDITIONER','HAIR SPRAY'])]
    
            #Vaseline
            
            Vaseline = Nielsen_Raw_Data[Nielsen_Raw_Data['BRAND'].isin(['VASELINE (UNILEVER HOME & PERSONAL CARE)'])]
            Vaseline_1 = Vaseline[Vaseline['CATEGORY'].isin(['BODY','REMAINING HBL'])]

            BnW_Filted_Data = pd.concat([Dove_Haircare_3, Nexxus_3, sheamoisture_3, Tresemme_3, Vaseline_1])     
            download_csv_BnW(BnW_Filted_Data, label="Download BnW_Brands_Data (csv)")
            
            #Brayers

            Brayers_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Brayers_2 = Brayers_1[Brayers_1['BRAND'].isin(['BREYERS (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Brayers_3 = Brayers_2[Brayers_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]

            #Talenti

            Talenti_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Talenti_2 = Talenti_1[Talenti_1['BRAND'].isin(['TALENTI (TALENTI GELATO)'])]
            Talenti_3 = Talenti_2[Talenti_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]

            #Klondike

            Klondike_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Klondike_2 = Klondike_1[Klondike_1['BRAND'].isin(['KLONDIKE (GOOD HUMOR-BREYERS ICE CREAM)'])]
            Klondike_3 = Klondike_2[Klondike_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]
            
            #Yasso

            Yasso_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Yasso_2 = Yasso_1[Yasso_1['BRAND'].isin(['YASSO (YASSO INC)'])]
            Yasso_3 = Yasso_2[Yasso_2['CATEGORY'].isin(['ICE CREAM','FROZEN NOVELTY'])]

            #Hellmanns

            Hellmanns_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Hellmanns_2 = Hellmanns_1[Hellmanns_1['BRAND'].isin(['BEST FOODS (UNILEVER BESTFOODS)',"HELLMANN'S (UNILEVER BESTFOODS)"])]
            Hellmanns_3 = Hellmanns_2[Hellmanns_2['CATEGORY'].isin(['MAYONNAISE'])]

            #knorr

            Knorr_1 = Nielsen_Raw_Data[Nielsen_Raw_Data['Market Description'].isin(['Total US xAOC'])]
            Knorr_2 = Knorr_1[Knorr_1['BRAND'].isin(['KNORR (UNILEVER BESTFOODS)'])]
            Knorr_3 = Knorr_2[Knorr_2['CATEGORY'].isin(['BOUILLON','RICE','PASTA','SHELF STABLE MEAL KIT'])]

            NIC_Filted_Data = pd.concat([Brayers_3, Talenti_3, Klondike_3, Yasso_3, Hellmanns_3,Knorr_3])     
            download_csv_NIC(NIC_Filted_Data, label="Download NIC_Brands_Data (csv)")
            

            # Checkbox to enable/disable sidebar filters
            enable_filters = st.checkbox("Enable Sidebar Filters and Pivot Table")

            # Enable sidebar filters if checkbox is checked
            if enable_filters:
                filtered_data = sidebar_filters(Nielsen_Raw_Data)
                st.write("Filtered Data:")
                st.write(filtered_data)
                download_csv_raw(filtered_data, label="Download Filtered_Raw_Data (CSV)", filename='Filtered_Raw_Data.csv')

                # Generate pivot table from filtered data
                pivot_table = generate_pivot_table(filtered_data)
                st.write("Pivot Table:")
                st.write(pivot_table)
                download_csv_raw(pivot_table, label="Download Pivot_Table_Data (CSV)", filename='Pivot_Table_Data.csv')
                

    if __name__ == "__main__":
        main()

    # Add content for Nielsen here
elif selected == "Playground":
    st.subheader(f"You have selected {selected}")

    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}


    def download_xlsx(df, label, filename):
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        st.download_button(label=label, data=excel_file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def download_csv(df, label, filename):
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        csv_file.seek(0)
        st.download_button(label=label, data=csv_file, file_name=filename, mime="text/csv")

    def sidebar_filters_1(data):
        
        st.sidebar.header("Filter for combined RROI File")
        Brand = st.sidebar.multiselect("Select the Brand:",options=data["Brand"].unique(),)
        data = data[data["Brand"].isin(Brand)]
        year = st.sidebar.multiselect("Select the Year:",options=data["Year"].unique(),)
        data = data[data["Year"].isin(year)]
        Month = st.sidebar.multiselect("Select the Month:",options=data["Month"].unique(),)
        data = data[data["Month"].isin(Month)]
        
        return data

    def generate_pivot_table_1(filtered_data):

        filtered_data['Cost'] = pd.to_numeric(filtered_data['Cost'], errors='coerce')
        filtered_data['Impression'] = pd.to_numeric(filtered_data['Impression'], errors='coerce')
        filtered_data = filtered_data.dropna(subset=['Cost', 'Impression'])
        pivot_table = filtered_data.pivot_table(index=['Brand','Year', 'Month'], values=['Cost', 'Impression'], aggfunc='sum')
        pivot_table.reset_index(inplace=False)
        return pivot_table

    def sidebar_filters_2(data):
        
        st.sidebar.header("Filter for AI RROI File")
        year = st.sidebar.multiselect("Select the Year:",options=data["Year"].unique(),key="year_multiselect")
        data = data[data["Year"].isin(year)]
        Month = st.sidebar.multiselect("Select the Month:",options=data["Month"].unique(),key="month_multiselect")
        data = data[data["Month"].isin(Month)]

        return data

    def generate_pivot_table_2(filtered_data):
        # Convert the 'Cost' and 'Impression' columns to numeric, forcing errors to NaN
        filtered_data['Cost'] = pd.to_numeric(filtered_data['Cost'], errors='coerce')
        filtered_data['Impression'] = pd.to_numeric(filtered_data['Impression'], errors='coerce')
        # Drop rows with NaN values in 'Cost' or 'Impression' columns
        filtered_data = filtered_data.dropna(subset=['Cost', 'Impression'])
        # Generate the pivot table
        pivot_table = filtered_data.pivot_table(index=['Year', 'Month'], values=['Cost', 'Impression'], aggfunc='sum')
        # Reset the index to turn the pivot table into a regular DataFrame
        pivot_table.reset_index(inplace=False)
        return pivot_table
        
    with st.sidebar:
        initialize_session_state()
        selected = st.selectbox("Main Menu", ["Home", 'Dimensions Check','Metrics Check'], index=0)

    if selected == "Dimensions Check":
        st.subheader("Dimensions Check")
        Dimensions_Check = st.file_uploader("Upload your Excel file(s)", type=["xlsx"], accept_multiple_files=True)
        dataframes_check = []
        if Dimensions_Check:
            for file in Dimensions_Check:
                Dimensions_Check_df = pd.read_excel(file)
                dataframes_check.append(Dimensions_Check_df)
            st.write(Dimensions_Check_df)

        Dimensions_RROI = st.file_uploader("Upload your Csv file(s)", type=["csv"], accept_multiple_files=True)           
        dataframes_rroi = []
        if Dimensions_RROI:
            for file in Dimensions_RROI:
                Dimensions_RROI_df = pd.read_csv(file)
                dataframes_rroi.append(Dimensions_RROI_df)
            st.write(Dimensions_RROI_df)
        
            def display_unique_and_difference(column_name):
                present_values = Dimensions_Check_df.loc[Dimensions_Check_df[column_name].isin(Dimensions_RROI_df[column_name]), column_name].unique()
                st.write(f"Unique list of {column_name} present in both DataFrames:", present_values)
        
                rroi_not_in_check = Dimensions_RROI_df[~Dimensions_RROI_df[column_name].isin(Dimensions_Check_df[column_name])][column_name].unique()
                unique_list = ', '.join(map(str, rroi_not_in_check))
                # Adding color using HTML
                st.markdown(f"<p style='color:blue;'>Unique list of {column_name} in Playground_Check_list but not in Formatted_Playground_File:</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:Red;'>{unique_list}</p>", unsafe_allow_html=True)

            display_unique_and_difference('Organisation')
            display_unique_and_difference('Business Unit')
            display_unique_and_difference('Category')
            display_unique_and_difference('Sub category')
            display_unique_and_difference('Brand')
            display_unique_and_difference('Total Brand')
            display_unique_and_difference('Media Type')
            display_unique_and_difference('Product Line')
            display_unique_and_difference('Master Channel')
            display_unique_and_difference('Channel')
            display_unique_and_difference('Platform')
            display_unique_and_difference('Influencer Say')
            display_unique_and_difference('Color Code')
            display_unique_and_difference('Audience')
            display_unique_and_difference('Daypart')
            
    if selected == "Metrics Check":
        st.subheader("Metrics Check")
        Metrics_RROI = st.file_uploader("Upload your Combine RROI file", type=["csv"], accept_multiple_files=True)
        Metrics_df = []
        if Metrics_RROI:
            for file in Metrics_RROI:
                    Metrics_RROI_df = pd.read_csv(file)
                    Metrics_df.append(Metrics_RROI_df)
            st.write("Full Data:")
            st.write(Metrics_RROI_df)
        AI_RROI_File = st.file_uploader("Upload your AI RROI file", type=["xlsx"], accept_multiple_files=True)
        AI_RROI_check = []
        if AI_RROI_File:
            for file in AI_RROI_File:
                AI_RROI_File_df = pd.read_excel(file)
                AI_RROI_check.append(AI_RROI_File_df)
            st.write(AI_RROI_File_df) 
            enable_filters = st.checkbox("Enable Sidebar Filters and Pivot Table")
            if enable_filters:
                Metrics_RROI_df = sidebar_filters_1(Metrics_RROI_df)   
                pivot_table = generate_pivot_table_1(Metrics_RROI_df)
                st.write("Combine RROI Pivot Table:")
                st.write(pivot_table)
                AI_RROI_File_df = sidebar_filters_2(AI_RROI_File_df)   
                pivot_table = generate_pivot_table_2(AI_RROI_File_df)
                st.write("AI RROI Pivot Table:")
                st.write(pivot_table)    
        # Add content for Playground here
elif selected == "DMS":
    st.subheader("Development Management System")
    uploaded_file = st.file_uploader("Choose a AI RROI Model Result File", type=['xlsx'])

    if uploaded_file is not None:
        # Process the uploaded file, e.g., read as pandas dataframe
        # Example: Read as pandas dataframe
        df = pd.read_excel(uploaded_file)
        # Display some information More More Feature More Feature the uploaded file
        st.write("### Uploaded the AI RROI Model Result File:")
        st.write(df)

       
elif selected == "QC":
    # Function to process JSON file to DataFrame
    def process_json_to_excel(json_file_path):
        with open(json_file_path) as file:
            data = json.load(file)
        
        new_data = {}
        for product_line in data:
            for master_channel in data[product_line]:
                new_data = {**new_data, **data[product_line][master_channel]}
        
        rows = []
        for feature, variables in new_data.items():
            if isinstance(variables, list):
                for var in variables:
                    rows.append({'Features': feature, 'Variables': var})
            else:
                rows.append({'Features': feature, 'Variables': variables})
        
        return pd.DataFrame(rows)

    # Function to initialize session state
    def initialize_session_state():
        if 'modified_files' not in st.session_state:
            st.session_state.modified_files = {}

    with st.sidebar:
        initialize_session_state()
        selected = st.selectbox("Main Menu", ['Json to Excel'], index=0)

    st.header("Quality Check")


    if selected == 'Json to Excel':
        st.header("Convert Json files to Excel files")
        uploaded_files = st.file_uploader("Upload JSON file(s)", type="json", accept_multiple_files=True)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save uploaded file to a temporary location
                with open("temp.json", "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Process JSON file
                df = process_json_to_excel("temp.json")
                
                # Save DataFrame to Excel file
                excel_file = BytesIO()
                df.to_excel(excel_file, index=False)
                excel_file.seek(0)
                
                # Download Excel file
                st.download_button(label=f"Download Excel File ({uploaded_file.name})", data=excel_file, file_name=f'output_{uploaded_file.name}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                # Delete temporary JSON file
                os.remove("temp.json")


    sys.exit()

    # Add content for QC here
elif selected == "Setting":
    st.title(f"You have selected {selected}")
    # Add content for Setting here
elif selected == "More Feature":
    st.title(f"You have selected {selected}")
    # Add content for More Feature Feature here
