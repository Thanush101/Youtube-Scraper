#!/bin/bash
# Set environment variables
export RENDER=true
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers

# Start the application
gunicorn app:app --bind 0.0.0.0:$PORT 