#!/bin/bash

set -euo pipefail

python ./manage.py test -t .
