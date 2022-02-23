#!/bin/bash

# Checks to see if first run to establish initial SSH check
FILE=/root/first.txt
if [ ! -f "$FILE" ];
then
    ssh -o StrictHostKeyChecking=no $1 "true"
    touch /root/first.txt
fi

echo "Running python"
python3 /root/ingestion.py /root/config.toml