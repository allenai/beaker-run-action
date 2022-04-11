FROM python:3.10-alpine

WORKDIR /app/beaker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY beaker_run.py .

ENTRYPOINT ["python", "/app/beaker/beaker_run.py"]
