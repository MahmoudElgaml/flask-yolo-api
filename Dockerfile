FROM python:3.12-slim

# Install OpenCV dependencies (including libGL.so.1)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to the container
COPY . .

# Set environment variables (optional)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the correct port (default Flask port is 5000)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
