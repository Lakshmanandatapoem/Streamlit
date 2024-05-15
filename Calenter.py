import datetime
import streamlit as st

# Function to advance the date by a given number of days
def advance_date(date, days):
    return date + datetime.timedelta(days=days)

# Function to advance the date by a given number of months
def advance_month(date, months):
    year = date.year + (date.month + months - 1) // 12
    month = (date.month + months - 1) % 12 + 1
    day = min(date.day, [31,
                         29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                         31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime.date(year, month, day)

# Function to advance the date by a given number of years
def advance_year(date, years):
    year = date.year + years
    return datetime.date(year, date.month, date.day)

# Main Streamlit code
def main():
    # Add custom CSS for background image
    st.markdown(
        """
        <style>
        body {
            background-image: url("https://images.pexels.com/photos/531880/pexels-photo-531880.jpeg?cs=srgb&dl=background-blur-clean-531880.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Calendar")
    d = st.date_input("Select a date", value=datetime.date.today())
    st.write("Selected date:", d)

    st.write("Advance the calendar:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Previous Day"):
            d = advance_date(d, -1)
    with col2:
        if st.button("Next Day"):
            d = advance_date(d, 1)
    with col3:
        if st.button("Next Month"):
            d = advance_month(d, 1)
    with col4:
        if st.button("Previous Month"):
            d = advance_month(d, -1)
            
    st.write("Updated date:", d)

    # Additional options for advancing by year
    st.write("Advance by year:")
    col5, col6 = st.columns(2)
    with col5:
        if st.button("Previous Year"):
            d = advance_year(d, -1)
    with col6:
        if st.button("Next Year"):
            d = advance_year(d, 1)
    
    st.write("Updated date:", d)

if __name__ == "__main__":
    main()
