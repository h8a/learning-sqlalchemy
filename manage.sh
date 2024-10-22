#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1

APP_NAME=learning-sqlalchemy

ENV_FILE=.env

PACKAGES=.venv

BASE_DIR=$(pwd)

BASE_DIR_EXAMPLES="$BASE_DIR/src/examples"

EXERCISE=""

if [ ! -f $ENV_FILE ]; then
  cp example.env .env
fi

list_examples() {
  for file in "$BASE_DIR_EXAMPLES"/*.py; do
    filename=$(basename "${file%.py}")
    echo "- $filename"
  done
}

exercise() {
  export EXERCISE
  docker compose -p $APP_NAME \
    -f ./docker/docker-compose.yml \
    --env-file $ENV_FILE \
    up --build
}

install() {
  pipenv install
}

clean() {
  echo "Not implemented"
}

help() {
  echo """
Help Command - Usage Guide

DESCRIPTION:
This command provides information and guidance on how to use the available commands in the application.
Use this help command to understand the functionality of each feature and get examples for quick reference.

USAGE:
./manage.sh help

OPTIONS:
  help            Show help for a specific command or the list of all available commands.
  examples        List examples of code

EXAMPLES:
  1.- Display this example message
      ./manage.sh help

  2.- Display a list of possibles command and examples
      ./manage.sh examples

  3.- Execute example connection
      ./manage.sh connection

  4.- Execute example models
      ./manage.sh models
"""
}

case $1 in
"install")
  install
  ;;
"examples")
  list_examples
  ;;
"connection" | "models")
  EXERCISE=$1
  exercise
  ;;
*)
  help
  ;;
esac
