FROM python:3.11-slim
LABEL maintainer="radomir"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and activate a virtual environment
RUN python -m venv /py

# Set the PATH to use the venv as default
ENV PATH="/py/bin:$PATH"

# Copy the requirements file and install dependencies (and clean up unnecessary files after)
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    apt-get update && \
    apt-get install -y default-mysql-client && \
    rm /tmp/requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the application port
EXPOSE 80

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
