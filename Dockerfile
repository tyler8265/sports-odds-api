FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY src/ src/
COPY conftest.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
