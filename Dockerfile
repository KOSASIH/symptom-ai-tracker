FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create uploads directory if it doesn't exist
RUN mkdir -p static/uploads

EXPOSE 8080

CMD ["python", "app.py"]