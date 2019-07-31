#!/usr/bin/env bash

# Get certificates
if [ "$USE_ADMIN_CONFIG" -eq 1 ]; then
    mkdir -p ${CERT_PATH}

    curl -H "Authorization: X-TESLA $TESLA_TOKEN" -o ${CERT_PATH}/${SECRET_PREFIX}SERVER_CA ${ADMIN_URL}/api/v1/system/certificate/server/ca
    curl -H "Authorization: X-TESLA $TESLA_TOKEN" -o ${CERT_PATH}/${SECRET_PREFIX}SERVER_KEY ${ADMIN_URL}/api/v1/system/certificate/server/key
    curl -H "Authorization: X-TESLA $TESLA_TOKEN" -o ${CERT_PATH}/${SECRET_PREFIX}SERVER_CERT ${ADMIN_URL}/api/v1/system/certificate/server/certificate
fi

# Start uwsgi
uwsgi --emperor /etc/uwsgi/emperor.ini &

# Initialize Nginx configuration
envsubst '${INSTRUMENT_PORT}:${SECRET_PREFIX}' < /app/nginx.vh.default.conf > /etc/nginx/conf.d/default.conf

# Start Nginx
nginx