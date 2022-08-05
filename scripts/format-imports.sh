#!/bin/sh -e
set -x

isort ./app
sh ./scripts/format.sh
