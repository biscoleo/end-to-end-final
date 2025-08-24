FROM python:3.9-slim

WORKDIR /app

# install system deps for psycopg2 (Postgres driver)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# change so it doesn't conflict with other UI
EXPOSE 8502

CMD ["streamlit", "run", "dashboard.py", "--server.port=8502", "--server.address=0.0.0.0"]

