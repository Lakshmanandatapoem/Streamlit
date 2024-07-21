import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the CSS for the buttons and header
css = """
<style>
button {
 width: 7em;
 height: 3em;
 border-radius: 30em;
 font-size: 15px;
 font-family: inherit;
 border: none;
 position: relative;
 overflow: hidden;
 z-index: 1;
 box-shadow: 6px 6px 12px #c5c5c5,
             -6px -6px 12px #ffffff;
 margin: 5px;  /* Add margin to create space between buttons */
}

button::before {
 content: '';
 width: 0;
 height: 3em;
 border-radius: 30em;
 position: absolute;
 top: 0;
 left: 0;
 background-image: linear-gradient(to right, #0fd850 0%, #f9f047 100%);
 transition: .5s ease;
 display: block;
 z-index: -1;
}

button:hover::before {
 width: 9em;
}

.centered-header {
 text-align: center;
}
</style>
"""

# Add the CSS to the Streamlit app
st.markdown(css, unsafe_allow_html=True)

# Function to create a button with the given label and key
def create_button(label, key):
    button_html = f"""
    <button onclick="window.location.href='#{key}'">
        {label}
    </button>
    """
    st.markdown(button_html, unsafe_allow_html=True)

# Display centered header
st.markdown('<h2 class="centered-header">HR Visualization Dashboard</h2>', unsafe_allow_html=True)

# Display buttons
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    create_button("Overview", "overview")
with col2:
    create_button("Salary", "salary")
with col3:
    create_button("Demographics", "demographics")
with col4:
    create_button("Hires", "hires")
with col5:
    create_button("Training", "training")
with col6:
    create_button("Terminations", "terminations")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown("<hr>", unsafe_allow_html=True) 
    st.write(df)
else:
    st.write("Please upload a CSV file to proceed.")
