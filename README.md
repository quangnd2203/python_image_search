# python_image_search

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

Install Python version 3.11.0 via pyenv:
```bash
pyenv install 3.11.0
pyenv local 3.11.0
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
├── python_image_search/
│   └── (Your source code files)
```

## Usage

Activate your poetry environment:
```bash
poetry shell
```

Then run IPython or any scripts you want:
```bash
poetry run ipython
```

---

## Notes
- Always make sure you are inside the Poetry environment when installing new packages.
- If you switch the Python version with pyenv, recreate your Poetry environment:
```bash
poetry env use $(pyenv which python)
poetry install
```

---

## License
MIT License.

---

## Author
- Quang Nguyen