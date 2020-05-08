#!/bin/bash

USERS=$1
FILES_USERS=$2
SESSIONS=$3
FILES_SESSIONS=$4

python3 users_generator.py $USERS $FILES_USERS
python3 sessions_users_generator.py $SESSIONS $FILES_SESSIONS $USERS
python3 sessions_purchases_generator.py $SESSIONS $FILES_SESSIONS $USERS
