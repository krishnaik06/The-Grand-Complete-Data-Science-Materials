FROM nvidia/cuda:12.0.1-base-ubuntu22.04
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get update \
    && apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
# RUN python3 -c 'import nltk; nltk.download("punkt")'
EXPOSE 8001
CMD ["uvicorn", "summarize_fastapi:app", "--host=0.0.0.0", "--port=8001", "--reload"]