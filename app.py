import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Generative AI with API key
genai.configure(api_key=os.getenv('GOOGLE-API-KEY'))

# Prepare the front end with more structured layout
st.set_page_config(page_title="Image Captioner", layout="wide")  # Full-width layout

# Header and Title
st.header("Captions for Images", divider="grey")
st.title("🖼️ Image Captioner")

# Sidebar for user input (upload and camera)
with st.sidebar:
    st.subheader("Upload or Capture an Image")
    # Upload image
    file_upload = st.file_uploader("Upload your file here...", type=["JPG", "JPEG", "PNG"])
    
    # Camera input with toggle
    enable = st.checkbox("Enable Camera")
    picture = st.camera_input("Take a picture", disabled=not enable)

# Main Section for Input
st.subheader("Generate Captions with AI")

# Optional text prompt input
user_input = st.text_input("Input an optional text prompt for more specific captions")

# Display uploaded or captured image
img = None
if file_upload is not None:
    img = Image.open(file_upload)
    st.image(img, caption="Uploaded Image", use_column_width=True)
elif picture is not None:
    img = Image.open(picture)
    st.image(img, caption="Captured Image", use_column_width=True)
else:
    st.warning("Please upload or capture an image to generate a caption.")

# Improved function for generating captions using Google Generative AI (Gemini)
def generate_caption(user_input, img):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
    # Basic validation to ensure image exists
    if img is None:
        st.error("No image provided. Please upload or capture an image.")
        return None

    try:
        # If user input is provided, send both text and image
        if user_input.strip():
            st.info("Generating caption with custom prompt...")
            response = model.generate_content([user_input, img])  # Pass the image object directly
        else:
            st.info("Generating caption based on the image alone...")
            response = model.generate_content(img)  # Pass the image object directly
        
        return response.text
    
    except Exception as e:
        st.error(f"An error occurred while generating the caption: {e}")
        return None

# Submit button with clear label
submit = st.button("🔮 Generate Caption")

# Loading animation or spinner during model response
if submit and img is not None:
    with st.spinner("Generating caption..."):
        caption_response = generate_caption(user_input, img)
        if caption_response:
            st.subheader("📝 Generated Caption:")
            st.write(caption_response)
        else:
            st.error("Could not generate a caption. Please try again.")

# Instructions or Footer for the user
st.write("---")
st.caption("Tip: Add a prompt to guide the AI for more specific captions or just leave it blank for an automatic caption.")
