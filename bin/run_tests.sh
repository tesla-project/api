#!/usr/bin/env bash

cd ..

# export environment for database
export DB_NAME=$PWD/test.db
export DB_PORT=25432
export DB_PASSWORD=
export DB_ENGINE=sqlite
export FLASK_APP=manage.py

export TEP_DB_DATABASE=tep_inst_test
export TEP_DB_NAME=tep_inst_test
export TEP_DB_HOST=tesla-test-rds.cs8uz6zrm2dq.eu-west-1.rds.amazonaws.com
export TEP_DB_PORT=5432
export TEP_DB_USER=tep_inst_test
export TEP_DB_PASSWORD=u2374c43ptBIk99b5i
export TEP_DB_ENGINE=postgres


# remove older migrations
rm -rf migrations
# remove older test database
rm $DB_NAME

# create test database
flask db init
flask db migrate -m "Create DB with current models"

# patch SQLite for BigInteger: replace sa.BigInteger() for sa.Integer()
for filename in migrations/versions/*.py; do
    sed -i 's/sa.BigInteger()/sa.Integer()/g' $filename
done

flask db upgrade

# insert test_data
sqlite3 $DB_NAME < tesla_api/tests/db.sql

# test test and test
pytest -v