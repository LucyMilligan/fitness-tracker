FROM python:3.12-slim-bookworm

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--port", "8080"]