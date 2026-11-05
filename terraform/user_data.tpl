#!/bin/bash

# Install your Python environment
apt-get update -y
apt-get install -y python3.14-venv
python3.14 -m venv venv
source venv/bin/activate

# Clon the latest app directly onto the server
git clone https://github.com/naiamartin/calc_backend_v2.git
cd calc_backend_v2/backend
pip install -r ../requirements.txt

# Initialize the database
export DATABASE_URL='${database_url}'

# Run Uvicorn on port bound to all interfaces
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port ${app_port} > uvicorn.log 2>&1 &