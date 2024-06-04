# Use the official Python 3.8 slim image as the base image
FROM python:3.12-slim

ENV DATABASE_URL="postgresql://multichain:multichain@master:5432/multichain"
ENV TOKEN="as0i3ksa0E2FFl-VQ."

# Set the working directory within the container
WORKDIR /api

# Copy the necessary files and directories into the container
#COPY resources/ static/ util/ .env application.py requirements.txt /api-flask/
#COPY resources/ /api-flask/resources/
#COPY static/ /api-flask/static/
#COPY util/ /api-flask/util/
COPY requirements.txt /api

# Upgrade pip and install Python dependencies
RUN apt update \
    && apt -y install libpq-dev gcc \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["python", "app.py"]

COPY app.py /api/
