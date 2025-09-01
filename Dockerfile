FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command: run Flask app
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]
