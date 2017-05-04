#!/bin/sh
if [ -z "${COMPOSE_FILE}" ]; then
  echo "Set the environment variable COMPOSE_FILE"
else
  docker-compose -f ${COMPOSE_FILE} run django python manage.py makemessages \
    --ignore linprog_solver/templates/account --ignore htmlcov
fi
