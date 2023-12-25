# Python and Linux Version
ARG PYTHON_VERSION=3.10-slim-buster

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage
COPY ./requirements .

ARG BUILD_ENVIRONMENT=production

RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    # dependencies for building Python packages
    build-essential \
    # lightgbm dependencies
    libgomp1

# Configure server
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt

COPY --chown=django:django ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Working directory
WORKDIR /app

ADD . /app
