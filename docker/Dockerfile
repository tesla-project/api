FROM python:3-alpine3.7

MAINTAINER Xavier Baro <xbaro@uoc.edu>

ENV SECRET_PREFIX API
ENV INSTRUMENT_PORT 443
ENV FLASK_APP manage.py
ENV CERT_PATH /run/secrets
ENV MODULE_NAME API
ENV MODULE_VERSION RC1

RUN apk add --update --no-cache unzip wget cmake alpine-sdk\
      nginx bash git gcc g++ make openrc gettext libffi-dev linux-headers netcat-openbsd

# There is a conflict between PostgreSQL and Cryptography due to the use of LibreSSL vs OpenSSL
# Install PostgreSQL package
RUN apk add --update --no-cache postgresql-dev
RUN pip install --upgrade psycopg2==2.7.4
RUN apk del postgresql-dev

# Install PostgreSQL package
RUN apk add --update --no-cache openssl-dev
RUN pip install pyOpenSSL==17.5.0
RUN apk add --no-cache postgresql-client

RUN pip install --upgrade pip==9.0.3
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uWSGI

# Copy configuration files
COPY docker/conf/emperor /etc/uwsgi
COPY docker/conf/nginx.vh.default.conf /app/
COPY docker/conf/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/service_uwsgi /logs

# setup application
WORKDIR /app
COPY manage.py .

# Copy the start script
COPY bin/run_service.py .

# Create running folder for Nginx
RUN mkdir /run/nginx

# Prepare starting script
COPY bin/start_service.sh .
RUN chmod +x start_service.sh

# Copy the api code
COPY tesla_api tesla_api

ENTRYPOINT ["/bin/bash"]
CMD ["/app/start_service.sh"]

RUN mkdir -p /app/data
