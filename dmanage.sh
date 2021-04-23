#!/bin/bash

docker-compose exec backend ./src/manage.py "$@"
