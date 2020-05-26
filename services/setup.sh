#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Error: Usage: setup.sh <module>"
    exit 1
fi

module=$1
local_modules="infrastructure webserver job_scheduler"
remote_modules="airflow_webserver airflow_scheduler airflow_worker mongo flower postgres governance dag_admin"

echo "Setting up module $module..."
if [ $module == 'local' ]; then
    docker-compose build --parallel $local_modules && docker-compose up -d $local_modules
elif [ $module == 'remote' ]; then
    # Generate unique fernet key for this Airflow installation
    export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    sudo docker-compose build --parallel $remote_modules && sudo docker-compose up -d $remote_modules
else
    echo "Module $module not supported"
    exit 1
fi
