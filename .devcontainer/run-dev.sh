#!/bin/bash

# This script will run the Django development server and the Tailwind CSS compiler in parallel.
# It will also ensure that both processes are terminated when the script exits.
trap "kill 0" EXIT

python manage.py tailwind start &
python manage.py runserver &

wait