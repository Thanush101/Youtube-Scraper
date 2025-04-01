# YouTube Scraper

A web application that scrapes YouTube playlists and videos based on search queries.

## Deployment to Render

Follow these steps to deploy this application to Render:

1. Create a Render account at https://render.com
2. Connect your GitHub account to Render
3. Create a new Web Service and select your repository
4. Use the following settings:
   - Environment: Python
   - Build Command: `./build.sh`
   - Start Command: `./start.sh`

Render will automatically detect the `requirements.txt` file and install the dependencies.

## Manual Deployment

Alternatively, you can deploy manually using these steps:

1. Fork or clone this repository
2. Create a new Web Service on Render
3. Connect to your GitHub repository
4. Set the build command to: `pip install -r requirements.txt && python -m playwright install chromium && mkdir -p output`
5. Set the start command to: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Set the Python version to 3.9 or later

## Local Development

To run this application locally:

```
pip install -r requirements.txt
python -m playwright install chromium
python app.py
```

Visit http://localhost:5000 in your browser. 