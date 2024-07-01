# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Run migrations and collect static files
RUN python manage.py migrate

RUN python manage.py collectstatic --noinput
RUN python manage.py createsuperuser

# Expose the port the app runs on
EXPOSE 8000

# Start Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
