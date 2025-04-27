#!/bin/bash
# wait-for-mysql.sh

while ! exec 6<>/dev/tcp/mysql-db/3306; do
    echo "Trying to connect to MySQL at 3306..."
    sleep 5
done
