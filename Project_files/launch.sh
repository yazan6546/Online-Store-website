#!/bin/bash

# Set the base directory to the directory where the script is located
BASEDIR=$(cd "$(dirname "$0")" && pwd)

echo $BASEDIR
echo "Starting Flask application..."

# Load environment variables from .flaskenv
set -a
source "$BASEDIR/.flaskenv"
set +a

# Run the Flask application
flask run