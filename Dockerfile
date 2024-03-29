FROM python:3.11-slim-bookworm

WORKDIR /src

COPY ./core/requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY src/ ./src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]