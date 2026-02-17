FROM python:3.11-slim

WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app ./app

# expose port
EXPOSE 8000

# start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
