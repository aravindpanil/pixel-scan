# Use slim Python base
FROM python:slim

# Set working directory in container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app directly from root
CMD ["python", "main.py"]