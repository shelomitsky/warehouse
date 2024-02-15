FROM python:3.9-slim

WORKDIR /app
ENV FLASK_APP main.py
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]