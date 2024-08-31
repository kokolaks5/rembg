import streamlit as st
from rembg import remove
# from PIL import Image

import requests

# --- HERO SECTION ---

st.markdown("[![100pa.com](https://www.100pa.com/images/logo.png)](https://100pa.com/)")
st.title("Remove background from image")

st.markdown("Paste the image URL or upload a file from your computer")

obraz_url = st.text_input("URL image: ")
obraz_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg", "bmp", "tiff", "webp", "jfif"])

if obraz_file is not None:
    obraz = obraz_file.read()
elif obraz_url:
    obraz = requests.get(obraz_url).content
else:
    st.error("Please paste a valid image URL or upload a file from your computer.")
    st.stop()

st.write("Original image")
st.image(obraz)

st.write("Parameters")
model = st.selectbox("Model", ["u2net_human_seg", "u2net"])
alpha_matting = st.slider("Background Removal Adjustment", 0.0, 1.0, 0.0, 0.01)
alpha_matting_foreground_threshold = st.slider("Foreground threshold", 0.0, 1.0, 0.96, 0.01)
alpha_matting_background_threshold = st.slider("Background Threshold", 0.0, 1.0, 0.02, 0.01)

obraz_bez_tla = remove(obraz, 
                       model=model, 
                       alpha_matting=alpha_matting, 
                       alpha_matting_foreground_threshold=alpha_matting_foreground_threshold, 
                       alpha_matting_background_threshold=alpha_matting_background_threshold)


st.write("Image without background")
st.image(obraz_bez_tla)

st.download_button(
    label="Download image without background",
    data=obraz_bez_tla,
    file_name="image_without_bg.png",
    mime="image/png"
)