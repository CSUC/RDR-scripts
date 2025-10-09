FROM python:3.11-slim

# Optional: install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy source
COPY create_Readme.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command
CMD ["python", "create_Readme.py"]