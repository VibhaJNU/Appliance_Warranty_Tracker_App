#use the official Python image as the base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the source code to the container
ADD src /app/

# Install any needed Python packages
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501
", "--server.address=0.0.0.0"]

