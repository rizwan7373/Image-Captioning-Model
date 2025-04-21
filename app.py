import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure Generative AI with API key
api_key = os.getenv("GOOGLE-API-KEY")
if not api_key:
    st.error("❌ API key not found. Please set GOOGLE-API-KEY in your environment.")
    st.stop()

genai.configure(api_key=api_key)

# App UI
st.set_page_config(page_title="Image Captioner", layout="wide")
st.header("Captions for Images", divider="grey")
st.title("🖼️ Image Captioner")

# Sidebar: Upload or Capture Image
with st.sidebar:
    st.subheader("Upload or Capture an Image")
    file_upload = st.file_uploader("Upload your file here...", type=["jpg", "jpeg", "png"])
    enable = st.checkbox("Enable Camera")
    picture = st.camera_input("Take a picture", disabled=not enable)

# Optional user text prompt
st.subheader("Generate Captions with AI")
user_input = st.text_input("Input an optional text prompt for more specific captions")

# Select image
img = None
if file_upload is not None:
    img = Image.open(file_upload).convert("RGB")
    st.image(img, caption="📤 Uploaded Image", use_column_width=True)
elif picture is not None:
    img = Image.open(picture).convert("RGB")
    st.image(img, caption="📸 Captured Image", use_column_width=True)
else:
    st.warning("Please upload or capture an image to generate a caption.")

# Caption generation function
def generate_caption(user_input, img):
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')

        # Convert PIL Image to byte stream (what Gemini expects)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Create proper input
        image_part = {
            "mime_type": "image/png",
            "data": img_bytes
        }

        if user_input.strip():
            st.info("Generating caption with your prompt...")
            response = model.generate_content([user_input, image_part])
        else:
            st.info("Generating caption based on the image only...")
            response = model.generate_content(image_part)

        return response.text

    except Exception as e:
        st.error(f"❌ Error while generating caption: {e}")
        return None

# Generate button
if st.button("🔮 Generate Caption") and img is not None:
    with st.spinner("Generating caption..."):
        caption = generate_caption(user_input, img)
        if caption:
            st.subheader("📝 Generated Caption:")
            st.write(caption)
        else:
            st.error("Caption could not be generated. Please try again.")

# Footer
st.write("---")
st.caption("💡 Tip: Use a prompt to guide the AI (like 'Describe this image like a movie scene').")
