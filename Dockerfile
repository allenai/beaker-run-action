FROM ghcr.io/allenai/beaker-py:v1.10.1

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY beaker_run.py .

ENTRYPOINT ["python", "/app/beaker/beaker_run.py"]
