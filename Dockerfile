FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "api.api:api", "--reload", "--host", "0.0.0.0", "--port", "8000"]