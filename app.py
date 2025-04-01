from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from Youtube_scraperV3 import scrape_youtube
import os
import json
import glob
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Ensure the output directory exists
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ensure templates directory exists
TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

def get_latest_json_file():
    """Get the most recently created JSON file in the output directory."""
    json_files = glob.glob(os.path.join(OUTPUT_DIR, "youtube_data_*.json"))
    if not json_files:
        return None
    return max(json_files, key=os.path.getctime)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    course_name = request.form.get('course_name')
    if not course_name:
        return jsonify({'error': 'Course name is required'}), 400
    
    try:
        # Run the scraper
        scrape_youtube(course_name, OUTPUT_DIR)
        
        # Get the latest JSON file
        json_file = get_latest_json_file()
        print(f"Latest JSON file: {json_file}")  # Debug print
        
        if not json_file or not os.path.exists(json_file):
            return jsonify({'error': 'Failed to find the generated JSON file'}), 500
        
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert videos data to DataFrame
        if not data.get('videos'):
            return jsonify({'error': 'No video data found'}), 500
            
        df = pd.DataFrame(data['videos'])
        
        # Generate CSV filename with timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"{secure_filename(course_name)}_{timestamp}_results.csv"
        csv_filepath = os.path.join(OUTPUT_DIR, csv_filename)
        
        # Save to CSV with all available columns
        columns_to_save = ['title', 'url', 'channel', 'duration', 'views', 'upload_time']
        df_to_save = df.reindex(columns=columns_to_save)
        df_to_save.to_csv(csv_filepath, index=False, encoding='utf-8')
        
        # Get just the filenames for the response
        json_filename = os.path.basename(json_file)
        
        return jsonify({
            'success': True,
            'message': 'Scraping completed successfully',
            'csv_file': csv_filename,
            'json_file': json_filename
        })
    
    except Exception as e:
        print(f"Error in scrape route: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        # Get the absolute path of the file
        file_path = os.path.join(OUTPUT_DIR, secure_filename(filename))
        print(f"Attempting to download: {file_path}")  # Debug print
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")  # Debug print
            return jsonify({'error': 'File not found'}), 404
        
        # Determine the file type and set appropriate mimetype
        mimetype = 'text/csv' if filename.endswith('.csv') else 'application/json'
            
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
    except Exception as e:
        print(f"Error in download route: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/files')
def list_files():
    """List all available files in the output directory."""
    try:
        files = []
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith('.json') or file.endswith('.csv'):
                files.append({
                    'name': file,
                    'path': os.path.join(OUTPUT_DIR, file),
                    'size': os.path.getsize(os.path.join(OUTPUT_DIR, file)),
                    'modified': os.path.getmtime(os.path.join(OUTPUT_DIR, file))
                })
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
