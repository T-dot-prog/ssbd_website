# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install LibreOffice in linux distributions
RUN apt-get update && apt-get install -y libreoffice 
RUN apt-get update && apt-get install -y fonts-dejavu fontconfig
COPY font /usr/share/fonts/truetype/custom/
RUN fc-cache -fv

# Copy the rest of the application code
COPY . .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
