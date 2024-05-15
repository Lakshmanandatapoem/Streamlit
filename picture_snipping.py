import streamlit as st
from PIL import Image

def snip_image(image, box):
    """
    Function to snip a portion of the image based on box coordinates.
    """
    left, top, right, bottom = box
    snipped_image = image.crop((left, top, right, bottom))
    return snipped_image

def main():
    st.title("Picture Snipping App")
    
    # Upload image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Get snipping coordinates from user
        st.write("Enter coordinates for snipping (left, top, right, bottom):")
        left = st.number_input("Left", value=0)
        top = st.number_input("Top", value=0)
        right = st.number_input("Right", value=image.width)
        bottom = st.number_input("Bottom", value=image.height)

        if st.button("Snip"):
            # Snip the image
            box = (left, top, right, bottom)
            snipped_image = snip_image(image, box)
            
            # Display the snipped image
            st.image(snipped_image, caption="Snipped Image", use_column_width=True)

if __name__ == "__main__":
    main()
