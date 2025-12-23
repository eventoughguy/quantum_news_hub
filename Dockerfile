FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5001

# Set environment variables
ENV FLASK_APP=project/news_agent/enhanced_app.py
ENV FLASK_ENV=production

# Create necessary directories and files
RUN mkdir -p project/news_agent
RUN touch project/news_agent/quantum_news_rss.db

WORKDIR /app/project/news_agent

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "enhanced_app:app"]