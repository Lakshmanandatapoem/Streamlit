import streamlit as st
import time

st.header("Task Streaming")
# Function to perform a time-consuming task
def perform_task():
    for i in range(1, 11):
        # Simulate the task completion percentage
        progress_percent = i * 10
        
        # Write progress updates to the stream
        st.text(f"Task Progress: {progress_percent}%")
        
        # Simulate a delay
        time.sleep(1)

# Trigger the task when a button is clicked
if st.button("Start Task"):
    perform_task()
