import streamlit as st

def main():
    st.title("Color Selector App")
    
    # Display a color picker widget
    selected_color = st.color_picker("Select a color", "#ff6347")  # Default color: Tomato
    
    # Display the selected color
    st.write("You selected:", selected_color)
    
if __name__ == "__main__":
    main()
