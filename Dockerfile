# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure static and media directories exist and are writable
RUN mkdir -p /app/static /app/media && chmod -R 777 /app/static /app/media

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 1234

# Run entrypoint script on container start
ENTRYPOINT ["/app/entrypoint.sh"]
