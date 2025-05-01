FROM python:3.10-alpine

WORKDIR /stage
RUN pip install --upgrade --no-cache-dir pip wheel build
COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

WORKDIR /app/beaker
RUN rm -rf /stage

COPY beaker_run.py .
ENTRYPOINT ["python", "/app/beaker/beaker_run.py"]
