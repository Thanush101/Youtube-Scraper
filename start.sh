#!/bin/bash
# Start the application using gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT 