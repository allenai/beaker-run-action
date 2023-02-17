FROM ghcr.io/allenai/beaker-py:latest

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

WORKDIR /app/beaker

COPY beaker_run.py .

ENTRYPOINT ["python", "/app/beaker/beaker_run.py"]
