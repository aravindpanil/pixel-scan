# Use slim Python base
FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app using Flask
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers", "5", "--timeout", "30", "--max-requests", "1000", "--max-requests-jitter", "50"]