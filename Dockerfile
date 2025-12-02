FROM python:3.13-slim AS builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.13-slim
WORKDIR /app

COPY --from=builder /install /usr/local

ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app/

WORKDIR ./

#Fixe entrypoint
ENTRYPOINT ["python"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000 

