#!/bin/bash
set -e



if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname lap \
    --lastname thanh \
    --role Admin \
    --email tuilathanhnha@gmail.com \
    --password admin
fi

$(command -v airflow) db upgrade

exec airflow webserver