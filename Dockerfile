# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose necessary ports
EXPOSE 22 80 443 5000

# Run the dashboard on container startup
CMD ["python", "dashboard/app.py"]
