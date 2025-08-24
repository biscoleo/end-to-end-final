# lightweight Python image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the app
COPY . .

# expose Streamlit default port
EXPOSE 8501

# run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
