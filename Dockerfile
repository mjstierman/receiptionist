# Use the official Python 3.13 image
FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
RUN apt-get update && apt-get install -y sqlite3
COPY src/requirements.txt ./

# Install python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Clone CS50's library from GitHub for usage in the application
RUN git clone https://github.com/cs50/python-cs50.git && \
    pip install ./python-cs50

# Copy the rest of the application source
COPY src/ ./

# Create the database if it doesn't exist
RUN if [ ! -f app.db ]; then \
    sqlite3 app.db < static/schema.sql; \
    fi

# Expose the necessary ports
EXPOSE 8000

# Start Gunicorn
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 app:app"]