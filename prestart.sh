#! /usr/bin/env bash

# Let the DB start
python ./app/backend_pre_start.py

# Create initial data in DB
python ./app/initial_data.py
