FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm \
    && npm install && npm run build:css \
    && apt-get remove -y nodejs npm && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
