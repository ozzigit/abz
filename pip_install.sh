#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
#pip install psycopg2-binary --no-binary psycopg2-binary # for arm64 bug
pip install -r requirements.txt
# db commands
export FLASK_APP=run.py
#export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
flask init_db
