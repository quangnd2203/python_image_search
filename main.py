"""
Image Search with CLIP Embeddings (Streamlit App)

This app allows users to initialize image embeddings from a local gallery and 
upload an image to compare against the gallery using cosine distance.
"""

import os
import io
import json
import base64
from PIL import Image
import streamlit as st

import llm
from scipy.spatial.distance import cosine
from src.translation import t

# ===================== Streamlit Config and Language =====================
st.set_page_config(
    page_title="Image Search",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.sidebar.markdown("## Settings")
lang_code = st.sidebar.selectbox("🌐 Language", ["en", "ja"], index=1)
st.session_state["lang"] = lang_code

# ===================== Model Load =====================
def load_model():
    return llm.get_embedding_model("clip")

model = load_model()

# ===================== File System Helpers =====================
def get_image_paths():
    return [f for f in os.listdir("assets") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

def is_db_initialized():
    return os.path.exists("db.json")

init_done = is_db_initialized()

# ===================== Utility Functions =====================
def img_to_base64(image):
    # Convert a PIL Image to a base64-encoded PNG string
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ===================== Streamlit Setup =====================
st.title(t("gallery_title", lang_code))

# ===================== Image Rendering =====================
def render_init_notice():
    # Render a notice prompting the user to initialize embeddings
    st.markdown(
        t("init_notice", lang_code)
    )

def render_upload_ui():
    # Render the image upload UI component and return the uploaded file if any
    st.markdown(t("upload_prompt", lang_code))
    return st.file_uploader(t("choose_image", lang_code), type=["jpg", "jpeg", "png"])

def render_image_grid(image_paths, scores: dict[str, float] = None):
    # Render a grid of images from the given file paths
    st.markdown(t("gallery_images", lang_code))
    cols = st.columns(3)  # Adjust number of columns as needed
    for i, img_path in enumerate(image_paths):
        img = Image.open(os.path.join("assets", img_path)).convert("RGB")
        img.thumbnail((400, 300), Image.LANCZOS)
        new_img = Image.new("RGB", (400, 300), (255, 255, 255))
        new_img.paste(img, ((400 - img.width) // 2, (300 - img.height) // 2))
        with cols[i % 3]:
            caption = f"{img_path}"
            if scores and img_path in scores:
                # Show similarity as bold percentage – (1 - cosine distance) * 100
                caption += f" <span style='color:#000000; font-weight:bold;'>Similarity: {((1 - scores[img_path]) * 100):.1f}%</span>"
            st.image(new_img, width=400, use_container_width=False, clamp=False, channels="RGB", output_format="auto")
            st.markdown(caption, unsafe_allow_html=True)

def process_uploaded_image(uploaded_file):
    # Display the uploaded image in the app
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption=t("uploaded_image", lang_code), width=400)

# ===================== Embedding Logic =====================
def init_embeddings():
    # Build the embedding DB from all images in /assets – run once unless images change
    image_paths = get_image_paths()
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
    st.success(t("embeddings_saved", lang_code))
    st.toast(t("embedding_completed", lang_code), icon="🎉")

# ===================== Uploaded Image Embedding =====================
def handle_uploaded_image_embedding(image_file):
    # Convert uploaded image to embedding vector and stash it for later matching
    image = Image.open(image_file).convert("RGB")
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        img_bytes = output.getvalue()
    embedding = list(model.embed_batch([img_bytes]))[0]
    st.session_state["uploaded_embedding"] = embedding
    return embedding

# ===================== Upload Handling =====================
def handle_upload():
    uploaded = render_upload_ui()
    if uploaded:
        st.session_state["uploaded_file"] = uploaded
    elif "uploaded_file" in st.session_state and st.session_state["uploaded_file"] is not None:
        st.session_state["uploaded_file"] = None

# ===================== Matching Logic =====================
def get_top_matches(uploaded_vec, db, threshold=0.3, top_k=3):
    # Compare uploaded image vector with gallery DB using cosine distance
    distances = []
    for name, vec in db.items():
        dist = cosine(uploaded_vec, vec)
        # Skip if distance is too high – not similar enough
        if dist <= threshold:
            distances.append((name, dist))
    # Sort by closest match
    distances.sort(key=lambda x: x[1])
    # Just grab the top-k most similar
    return distances[:top_k]

# ===================== Main Application Logic =====================
def main():
    # Run the app UI and flow
    render_init_notice()

    if st.button(t("init_button", lang_code), type="primary"):
        init_embeddings()
        st.rerun()

    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None

    if init_done:
        handle_upload()

    if not init_done:
        st.info(t("init_required_info", lang_code))
    else:
        if st.session_state["uploaded_file"]:
            process_uploaded_image(st.session_state["uploaded_file"])
            uploaded_vec = handle_uploaded_image_embedding(st.session_state["uploaded_file"])

            # Load database
            with open("db.json", "r") as f:
                db = json.load(f)

            top_matches_with_distances = get_top_matches(uploaded_vec, db, threshold=0.3, top_k=3)

            # Extract names and distances dict for rendering
            top_matches = [name for name, _ in top_matches_with_distances]
            distances_dict = {name: dist for name, dist in top_matches_with_distances}

            # Render only top matching images
            render_image_grid(top_matches, scores=distances_dict)

            return  # Skip rendering all images again
        else:
            image_paths = get_image_paths()
            render_image_grid(image_paths)

if __name__ == "__main__":
    main()
