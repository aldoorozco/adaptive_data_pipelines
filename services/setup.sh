#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Error: Usage: setup.sh <module>"
    exit 1
fi

module=$1
local_modules="infrastructure ui job_scheduler"
remote_modules="webserver scheduler worker mongo flower postgres governance dag_admin"

echo "Setting up module $module..."
if [ $module == 'local' ]; then
    export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    docker-compose build --parallel $local_modules && docker-compose up -d $local_modules
elif [ $module == 'remote' ]; then
    sudo docker-compose build --parallel $remote_modules && sudo docker-compose up -d $remote_modules
else
    echo "Module $module not supported"
    exit 1
fi
