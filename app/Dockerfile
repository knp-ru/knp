FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY app.py .
WORKDIR /app
# For local testing
EXPOSE 8081
CMD ["python", "app.py"]