#!/bin/bash
# Install Playwright browsers with dependencies
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers
playwright install chromium --with-deps
# Create the output directory
mkdir -p output 