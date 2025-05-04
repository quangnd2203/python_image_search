# python_image_search

> Updated to include structured Streamlit interface, image upload, grid display, and embedding initialization with persistence.

A project for image search and image embedding using CLIP models.

## Setup

This project uses **Poetry** for package management and **pyenv** for Python version management.

### Prerequisites
- Python 3.11.x (recommended)
- Poetry
- pyenv

### Install pyenv (if not installed)
```bash
brew install pyenv
```

Install Python version 3.11.x via pyenv:
```bash
pyenv install 3.11.x
pyenv local 3.11.x
```

### Install Poetry (if not installed)
```bash
brew install poetry
```

Configure Poetry to prefer the active Python from pyenv:
```bash
poetry env use $(pyenv which python)
```

### Install dependencies
In the project root:
```bash
poetry install
```

This installs the dependencies defined in `pyproject.toml`.

### Install CLIP model plugin
After installing dependencies, run:
```bash
poetry run llm install llm-clip
```

This will install the CLIP plugin for embeddings.

---

## Project Structure

```
python_image_search/
├── README.md
├── pyproject.toml
├── poetry.lock
├── db.json
├── assets/
├── main.py
└── src/
    ├── translation.py
    └── ...

```

## Usage

Activate your poetry environment:
```bash
poetry shell
```

Then run Streamlit app or any scripts you want:
```bash
poetry run streamlit run main.py
```

### How to Use the App

Before initializing, make sure the folder `assets/` exists in your project root. This is where you place the images to be embedded. You can manually create the folder if it doesn't exist:

```bash
mkdir -p assets
```

Then add any `.jpg` or `.png` images you'd like to compare.

When you first launch the app with `poetry run streamlit run main.py`, you will see a button labeled **"Init Embeddings"**.

- This will embed all existing images found in the `assets/` folder using the CLIP model.
- The embeddings will be saved to a local file `db.json`.
- The **Upload Image** button is disabled until embeddings are initialized to prevent invalid comparisons.

After that, you can upload new images to compare them with previously embedded ones. Uploaded images will be stored in session using `st.session_state["uploaded_file"]`. Images will be displayed in a grid layout, resized uniformly to 400x300, and wrapped in visible containers.

You must click "Init Embeddings" before uploading any image, or the upload option will be disabled.

---

## Notes
- Always make sure you are inside the Poetry environment when installing new packages.
- If you switch the Python version with pyenv, recreate your Poetry environment:
```bash
poetry env use $(pyenv which python)
poetry install
```
- To use this app effectively, always initialize embeddings before uploading new images.

---

## License
MIT License.

---

## Author
- Quang Nguyen