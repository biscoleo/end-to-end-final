# lightweight Python image
FROM python:3.9-slim

# system dependencies needed for psycopg2 and build tools
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /app

# copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code and other files
COPY . .

# expose FastAPI port
EXPOSE 8000

# run the FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
