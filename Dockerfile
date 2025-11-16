# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Environment setup
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .

# Install Python dependencies and system packages together
RUN pip install --no-cache-dir -r requirements.txt 

# Copy custom fonts (if any)
COPY font /usr/share/fonts/truetype/custom/
RUN fc-cache -fv

# Copy the rest of the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
