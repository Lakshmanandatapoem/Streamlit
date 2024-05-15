import streamlit as st

def main():
    st.title("HR Data Entry Form")
    
    # Sidebar for additional options
    st.sidebar.title("Options")
    show_data = st.sidebar.checkbox("Show Submitted Data")
    
    # Main form inputs
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        department = st.selectbox("Department", ["Engineering", "Sales", "Marketing", "Finance", "HR"])
    
    with col2:
        age = st.number_input("Age", min_value=0, max_value=50)
        address = st.text_area("Address")
        gender = st.radio("Gender", ["Male", "Female", "Other"])
    
    agree = st.checkbox("I agree to the terms and conditions")
    
    if st.button("Submit"):
        if agree:
            # Process the form data
            submitted_data = {
                "Name": name,
                "Age": age,
                "Email": email,
                "Phone Number": phone,
                "Address": address,
                "Department": department,
                "Gender": gender
            }
            st.write("Submitted Successfully!")
            st.write("Submitted Data:")
            st.write(submitted_data)
        else:
            st.warning("Please agree to the terms and conditions.")

    if show_data:
        st.subheader("Submitted Data")
        # Display previously submitted data
        # This can be stored in a database or a file
        # For simplicity, we're just showing the data submitted in the current session
        if "submitted_data" in locals():
            st.write(submitted_data)
        else:
            st.write("No data submitted yet.")

if __name__ == "__main__":
    main()
