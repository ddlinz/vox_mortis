#!/bin/bash

. /miniconda/etc/profile.d/conda.sh
conda activate vox_environment
pip install --upgrade flask-sqlalchemy
gunicorn -b 0.0.0.0:5000  -w 1 "vox.entry:app"
