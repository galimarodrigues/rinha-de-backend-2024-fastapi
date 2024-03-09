FROM python:3.11-slim-bookworm

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY src/api/ ./src/

CMD ["uvicorn", "src.api.app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]