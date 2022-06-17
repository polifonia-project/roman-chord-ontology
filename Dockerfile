FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./api /app/api

EXPOSE 80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
