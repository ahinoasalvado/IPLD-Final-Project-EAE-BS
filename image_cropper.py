# The libraries you have to use
import numpy as np
import streamlit as st
import io
from PIL import Image

# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to open, crop, display and save images using NumPy, PIL and Matplotlib.")

# ----- Title of the page -----
st.title("🖼️ Image Cropper")
st.divider()

# ----- Getting the image from the user or using the EAE image -----
img = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

if img is None:
    img = "eae_img.png"

# Open the image
with Image.open(img) as opened_img:
    img_arr = np.array(opened_img)

# Displaying the image
st.image(img_arr, caption="Original Image", use_container_width=True)
st.write("#")

# ----- Get min and max values for cropping -----
min_height = 0 
max_height = img_arr.shape[0]   # height (rows)
min_width = 0
max_width = img_arr.shape[1]    # width (columns)

# ----- Creating the sliders to receive user input -----
if isinstance(max_height, int) and isinstance(max_width, int):
    cols1 = st.columns([4, 1, 4])

    crop_min_h, crop_max_h = cols1[0].slider(
        "Crop Vertical Range",
        min_height, max_height,
        (int(max_height * 0.1), int(max_height * 0.9))
    )

    crop_min_w, crop_max_w = cols1[2].slider(
        "Crop Horizontal Range",
        min_width, max_width,
        (int(max_width * 0.1), int(max_width * 0.9))
    )

    st.write("## Cropped Image")

    # ----- Crop the image -----
    crop_arr = img_arr[crop_min_h:crop_max_h, crop_min_w:crop_max_w]

    # Displaying the cropped image and download option
    st.image(crop_arr, caption="Cropped Image", use_column_width=True)

    buf = io.BytesIO()
    Image.fromarray(crop_arr).save(buf, format="PNG")
    cropped_img_bytes = buf.getvalue()

    cols2 = st.columns([4, 1, 4])
    file_name = cols2[0].text_input("Choose a File Name:", "cropped_image") + ".png"

    st.download_button(
        label=f"Download the image `{file_name}`",
        data=cropped_img_bytes,
        file_name=file_name
    )

else:
    st.subheader("⚠️ Error detecting image dimensions.")

