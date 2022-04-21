FROM ghcr.io/allenai/beaker-py:v0.11.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY beaker_run.py .

ENTRYPOINT ["python", "/app/beaker/beaker_run.py"]
