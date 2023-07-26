FROM python:3.11-slim

ENV TZ=America/Sao_Paulo

WORKDIR /app

COPY . .

RUN apt-get update -y

RUN mkdir -p /app/out/log

RUN apt-get update -y && apt-get install -y curl gnupg gnupg1 gnupg2 
RUN apt-get install -y wget apt-transport-https

RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN echo "deb [arch=amd64] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y
RUN apt-get install -y unixodbc-dev libgssapi-krb5-2

ENV PATH="$PATH:/opt/mssql-tools18/bin"

RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python model_predict.py