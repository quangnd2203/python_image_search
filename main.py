import llm
import streamlit as st
import os
import io
from PIL import Image
import json
import base64

# ===================== Utility =====================
def img_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ===================== Model & Setup =====================
model = llm.get_embedding_model("clip")
init_done = os.path.exists("db.json")

st.set_page_config(
    page_title="Image Search",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Image Search")

# ===================== UI Components =====================
def render_init_notice():
    st.markdown(
        "### 📌 Before You Start\n"
        "Please click the **'Init embeddings'** button to generate and store image vectors. "
        "This step is necessary so the app can compare new images to existing ones."
    )

def render_upload_ui():
    st.markdown("### 📤 Upload Image to Compare")
    return st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def render_image_grid(image_paths):
    cols = st.columns(3)  # Adjust number of columns as needed
    for i, img_path in enumerate(image_paths):
        img = Image.open(os.path.join("assets", img_path)).convert("RGB")
        img.thumbnail((400, 300), Image.LANCZOS)
        new_img = Image.new("RGB", (400, 300), (255, 255, 255))
        new_img.paste(img, ((400 - img.width) // 2, (300 - img.height) // 2))
        with cols[i % 3]:
            st.image(new_img, caption=img_path, width=400)

def process_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=400)

# ===================== Embedding Logic =====================
def init_embeddings():
    image_paths = [f for f in os.listdir("assets") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    db = {}
    for img_path in image_paths:
        img = Image.open(os.path.join("assets", img_path))
        with io.BytesIO() as output:
            img.save(output, format="PNG")
            img_bytes = output.getvalue()
        embeddings = list(model.embed_batch([img_bytes]))
        if embeddings:
            db[img_path] = embeddings[0]
    with open("db.json", "w") as f:
        json.dump(db, f)
    st.success("Embeddings saved to db.json")
    st.toast("✅ Embedding completed and saved!", icon="🎉")

# ===================== Main =====================
def main():
    render_init_notice()

    if st.button("🚀 Init embeddings (Required before upload)", type="primary"):
        init_embeddings()
        st.rerun()

    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None

    if init_done:
        uploaded = render_upload_ui()
        if uploaded:
            st.session_state["uploaded_file"] = uploaded

    if not init_done:
        st.info("⚠️ Please click 'Init embeddings' first to enable image upload.")
    else:
        if st.session_state["uploaded_file"]:
            process_uploaded_image(st.session_state["uploaded_file"])

    # Always render the grid of images
    image_paths = [f for f in os.listdir("assets") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    render_image_grid(image_paths)

main()
