#!/bin/bash

set -e

mysql_user=banana
mysql_password=banana
mysql_host=localhost
mysql_db=predictive_alerting

python3 -m models
