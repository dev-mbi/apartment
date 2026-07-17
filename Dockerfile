FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN npm install && npm run build:css

RUN apt-get remove -y nodejs npm && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 5000

CMD ["./entrypoint.sh"]
