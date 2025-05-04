import streamlit as st

def main():
    lang = st.session_state.get("lang", "en")

    st.title(t("title", lang))

    if st.button(t("init_embeddings", lang)):
        # Initialization code here
        pass

    # Other Streamlit UI components using t(key, lang) for text

if __name__ == "__main__":
    main()

# translation.py

translations = {
    "en": {
        "before_start_title": "📌 Before You Start",
        "before_start_description": (
            "Please click the 'Init embeddings' button to generate and store image vectors. "
            "This step is necessary so the app can compare new images to existing ones."
        ),
        "init_embeddings_button": "📌 Init embeddings (Required before upload)",
        "init_button": "🚀 Init embeddings (Required before upload)",
        "upload_button": "Upload image",
        "init_success": "Embeddings saved to db.json",
        "gallery_title": "Gallery",
        "uploaded_image": "Uploaded Image",
        "settings_title": "Settings",
        "language_label": "Language",
        "init_notice": "📌 Before You Start\nPlease click the **'Init embeddings'** button to generate and store image vectors. \nThis step is necessary so the app can compare new images to existing ones.",
        "upload_prompt": "📤 Upload Image to Compare",
        "gallery_images": "🖼️ All Images in Gallery",
        "choose_image": "Choose an image...",
    },
    "ja": {
        "before_start_title": "📌 はじめに",
        "before_start_description": (
            "画像ベクトルを生成して保存するには「埋め込みを初期化」ボタンをクリックしてください。"
            "このステップは、新しい画像を既存の画像と比較するために必要です。"
        ),
        "init_embeddings_button": "📌 埋め込みを初期化（アップロード前に必須）",
        "init_button": "🚀 埋め込みを初期化（アップロード前に必須）",
        "upload_button": "画像をアップロード",
        "init_success": "ベクトルが db.json に保存されました",
        "gallery_title": "ギャラリー",
        "uploaded_image": "アップロードされた画像",
        "settings_title": "設定",
        "language_label": "言語",
        "init_notice": "📌 はじめに\n画像ベクトルを生成して保存するには「埋め込みを初期化」ボタンをクリックしてください。\nこのステップは、新しい画像を既存の画像と比較するために必要です。",
        "upload_prompt": "📤 比較する画像をアップロード",
        "gallery_images": "🖼️ ギャラリー内のすべての画像",
        "choose_image": "画像を選択してください...",
    }
}


def t(key: str, lang: str = "en") -> str:
    """Return translated string for a given key and language."""
    return translations.get(lang, translations["en"]).get(key, key)