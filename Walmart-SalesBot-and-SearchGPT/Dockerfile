FROM python:3.11-slim-buster AS build
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . .
FROM python:3.11-slim-buster AS runtime
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app .
EXPOSE 5000
CMD ["python3", "run_api.py", "--host", "0.0.0.0", "--port", "5000"]
