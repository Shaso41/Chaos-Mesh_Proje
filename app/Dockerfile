FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY backend.py .

# Expose port (will be overridden by docker-compose)
EXPOSE 5000 5001

# Default command
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
