#!/usr/bin/env bash
gunicorn -c gunicorn.py wsgi:app