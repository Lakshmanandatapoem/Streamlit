import streamlit as st
import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def main():
    st.title("Password Generator App")
    
    # Set default password length
    default_length = 12
    
    # Add a slider for password length
    password_length = st.slider("Select password length:", 4, 32, default_length)
    
    # Add a button to generate password
    if st.button("Generate Password"):
        password = generate_password(password_length)
        st.success("Your generated password is:")
        st.info(password)

if __name__ == "__main__":
    main()
