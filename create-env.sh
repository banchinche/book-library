#!/bin/bash

{

  echo "EMAIL_USE_TLS=$EMAIL_USE_TLS"

  echo "APP_NAME=${secrets.APP_NAME}"
  echo "MAIN_SUPERUSER=${secrets.MAIN_SUPERUSER}"
  echo "MAIN_SUPERUSER_PASSWORD=${secrets.MAIN_SUPERUSER_PASSWORD}"
  echo "POSTGRES_SERVER=${secrets.POSTGRES_SERVER}"
  echo "POSTGRES_PORT=${secrets.POSTGRES_PORT}"
  echo "POSTGRES_USER=${secrets.POSTGRES_USER}"
  echo "POSTGRES_PASSWORD=${secrets.POSTGRES_PASSWORD}"
  echo "POSTGRES_DB=${secrets.POSTGRES_DB}"
  echo "DATABASE_URI=${secrets.DATABASE_URI}"
  echo "JWT_ALGORITHM=${secrets.JWT_ALGORITHM}"
  echo "JWT_SECRET=${secrets.JWT_SECRET}"
} >> .env

{
  echo "POSTGRES_DB=${secrets.POSTGRES_DB}"
  echo "POSTGRES_USER=${secrets.POSTGRES_USER}"
  echo "POSTGRES_PASSWORD=${secrets.POSTGRES_PASSWORD}"
} >> .env.db
