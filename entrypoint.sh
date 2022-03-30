#!/bin/bash

if [ "$DATABASE" = "library" ]
then
    echo "Waiting for library database..."

    while ! nc -z "db" "5432"; do
      sleep 0.1
    done

    echo "Database started"
fi

sleep 30
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
