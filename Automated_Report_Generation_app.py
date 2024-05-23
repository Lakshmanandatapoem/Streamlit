import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import base64
import io

# Function to generate PDF report
def generate_report(data, title):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 12))

    # Convert DataFrame to list of lists
    data_list = [data.columns.to_list()] + data.values.tolist()

    # Define table
    table = Table(data_list, colWidths=[1.5 * inch] * len(data.columns))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    
    buffer.seek(0)
    return buffer

# Function to generate Excel report
def generate_excel(data):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    buffer.seek(0)
    return buffer

# Main function
def main():
    # Page title
    st.title("Automated Report Generation Version1")
    
    # Upload data
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        # Read CSV file with proper encoding
        data = pd.read_csv(uploaded_file, encoding='latin1')  # Change encoding if needed
        
        # Sidebar multi-select for filtering
        st.sidebar.title("Filter Options")
        unique_states = data['State'].unique()
        unique_regions = data['Region'].unique()
        
        selected_states = st.sidebar.multiselect("Select States", unique_states, default=unique_states)
        selected_regions = st.sidebar.multiselect("Select Regions", unique_regions, default=unique_regions)
        
        # Filter data based on selection
        filtered_data = data[data['State'].isin(selected_states) & data['Region'].isin(selected_regions)]
        
        # Display data
        st.subheader("Data")
        st.write(filtered_data)
        
        # Generate report button
        title = st.text_input("Enter Report Title", "My Report")
        if st.button("Generate Report"):
            # Generate PDF report
            pdf_buffer = generate_report(filtered_data, title)
            pdf_b64 = base64.b64encode(pdf_buffer.read()).decode()
            pdf_href = f'<a href="data:application/octet-stream;base64,{pdf_b64}" download="report.pdf">Download PDF Report</a>'
            st.markdown(pdf_href, unsafe_allow_html=True)
            
            # Generate Excel report
            excel_buffer = generate_excel(filtered_data)
            excel_b64 = base64.b64encode(excel_buffer.read()).decode()
            excel_href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_b64}" download="report.xlsx">Download Excel Report</a>'
            st.markdown(excel_href, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
