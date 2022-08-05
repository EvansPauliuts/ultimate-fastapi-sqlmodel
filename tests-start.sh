#! /usr/bin/env bash
set -e

exec poetry run bash ./scripts/test.sh "$@"
