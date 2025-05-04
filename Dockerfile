# Use official Python image
FROM python:alpine

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libgl1-mesa-glx libglib2.0-0 git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set path to poetry
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN poetry install --no-interaction --no-root && poetry run llm install llm-clip

# Expose Streamlit port
EXPOSE 8501

# Set entrypoint
CMD ["poetry", "run", "streamlit", "run", "src/python_image_search/main.py", "--server.port=8501", "--server.headless=true", "--server.enableCORS=false"]