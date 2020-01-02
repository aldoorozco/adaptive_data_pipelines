#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Error: Usage: setup.sh <module>"
    exit 1
fi

if [ ! -f "./credentials" ]; then
    echo "Error: Unable to locate AWS credentials in $PWD, please install and configure AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)"
    exit 1
fi

module=$1
local_modules="infrastructure ui job_scheduler"
remote_modules="webserver scheduler worker mongo flower postgres governance dag_admin"

echo "Setting up module $module..."
if [ $module == 'local' ]; then
    docker-compose build --parallel $local_modules && docker-compose up -d $local_modules
elif [ $module == 'remote' ]; then
    sudo docker-compose build --parallel $remote_modules && sudo docker-compose up -d $remote_modules
else
    echo "Module $module not supported"
    exit 1
fi
