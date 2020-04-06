#! /usr/bin/bash

## Resets the Project for Development Purposes

# Create Alias to manage.py Script
manage='./manage.py'

# Remove Migration Files
find . -wholename ".*migrations/*.py" -not -path ".*migrations/__init__.py" | xargs rm -f

# Remove Pycache Folders
find . -wholename ".*__pycache__" | xargs rm -rf

# Remove DB
rm db.sqlite3

# Make Migrations
$manage makemigrations

# Migrate 
$manage migrate

# Run Server
# $manage runserver