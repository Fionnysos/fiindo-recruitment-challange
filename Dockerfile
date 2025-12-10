FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run whole ETL pipeline as a module
CMD ["python", "-m", "src.run_pipeline"]
