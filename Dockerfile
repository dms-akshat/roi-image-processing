# Use official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 12345 for Django
EXPOSE 1234

# Ensure media and static folders exist
RUN mkdir -p /app/media/uploads /app/media/processed /app/static

# Run migrations and collect static files
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Start the Django application on port 1234
CMD ["gunicorn", "--bind", "0.0.0.0:1234", "image_processing.wsgi:application"]
