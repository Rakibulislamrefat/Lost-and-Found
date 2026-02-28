#!/bin/bash

# Install dependencies (Vercel uses uv-managed Python, needs --break-system-packages)
pip install --break-system-packages -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
