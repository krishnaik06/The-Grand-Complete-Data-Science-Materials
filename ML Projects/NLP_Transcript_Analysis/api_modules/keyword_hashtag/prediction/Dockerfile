FROM nvidia/cuda:12.0.1-base-ubuntu22.04
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get update \
    && apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
# RUN python3 -m spacy download en_core_web_sm
# RUN python3 -m spacy download en_core_web_md
# RUN python3 -c 'import nltk; nltk.download("punkt"); nltk.download("stopwords")'
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0.tar.gz --no-deps
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.5.0/en_core_web_md-3.5.0.tar.gz --no-deps
EXPOSE 8001
CMD ["uvicorn", "keyhash_fastapi:app", "--host=0.0.0.0", "--port=8001", "--reload"]