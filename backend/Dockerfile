# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PDF processing and OCR
RUN apt-get update && apt-get install -y \
	tesseract-ocr \
	libpoppler-dev \
	poppler-utils \
	ghostscript \
	build-essential \
	curl \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
	ln -s /root/.local/bin/poetry /usr/local/bin/

# Configure Poetry to not use a virtual environment inside the container
RUN poetry config virtualenvs.create false

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi --without dev

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
