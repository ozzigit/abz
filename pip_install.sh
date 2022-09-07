#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install psycopg2-binary --no-binary psycopg2-binary # for arm64 bug
pip install -r requirements.txt
export FLASK_APP=microblog.py