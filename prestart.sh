#! /usr/bin/env bash

# Let the DB start
poetry run python ./app/backend_pre_start.py

# Create initial data in DB
poetry run python ./app/initial_data.py
