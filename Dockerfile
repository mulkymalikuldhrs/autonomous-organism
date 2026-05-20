FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and dependencies
RUN playwright install --with-deps chromium

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Start the application
CMD ["python3", "-m", "backend.main"]
