FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV APP_MODULE app.main:app

#region Uncomment this below 2 line if you want to get package from Azure Artifact
# ARG INDEX_URL
# ENV PIP_EXTRA_INDEX_URL=$INDEX_URL
#endregion

COPY ./requirements.txt /app/requirements.txt

#region, this below region is to install pyodbc for Linux server, refer https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#18
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install --reinstall build-essential -y \
 && apt-get update \
 && apt install curl -y

RUN /bin/bash -c "curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
                && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list"

RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini
#endregion for pyodbc

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#region uncomment below line if you want to download spacy small model
# RUN spacy download en_core_web_sm

#region uncomment below lines if you want to download nltk data
# RUN python -m nltk.downloader punkt \
#     && python -m nltk.downloader stopwords \
#     && python -m nltk.downloader wordnet \
#     && python -m nltk.downloader omw-1.4

COPY ./app /app/app