#!/bin/bash

rm .containtername

timestamp=$(date +%s)
pgcontainer=e2e-postgres-$timestamp

echo $pgcontainer > .containtername

docker run --name $pgcontainer -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres;
sleep 5;

PGPASSWORD=mysecretpassword psql -U postgres -d postgres -c 'CREATE DATABASE amdb' -h localhost -p 5432;

cd ../..;
alembic upgrade head;

PGPASSWORD=mysecretpassword psql -U postgres -d amdb -c "INSERT INTO users VALUES ('a0f006db-7cfc-4335-a34f-e6b606341406', 'e2eadmin', decode('JDJiJDEyJC9GUGRROFFaS0J6Q0o1VlZLeE9ody5IR0VwVC5HWElkVmlqTU1uYjlpb0dmeElFaW1qVm9p', 'base64'), 1)" -h localhost -p 5432;
JWT_SECRET=mysecuresecret PERSISTENT_DB_CONNECTION_STRING=postgresql://postgres:mysecretpassword@localhost/amdb PERSISTENT_DB=true flask run > /dev/null 2>&1 &
cd -;

echo $! > .flaskpid;


