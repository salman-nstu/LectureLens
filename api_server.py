"""
AI Lecture Summarizer - Flask API Server
Handles HTTP requests for lecture summarization from various sources
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from summarization_service import process_lecture_input

# ==================== Application Configuration ====================
app = Flask(__name__)
CORS(app)

# Configuration constants
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'avi', 'mov', 'flac', 'm4a', 'webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================== Helper Functions ====================

def allowed_file(filename):
    """
    Check if uploaded file has an allowed extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_request_data(data):
    """
    Validate incoming request data
    
    Args:
        data: Request form data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    input_type = data.get("input_type")
    export_format = data.get("export_format")
    
    if not input_type:
        return False, "Missing required parameter: input_type"
    
    if not export_format:
        return False, "Missing required parameter: export_format"
    
    if input_type not in ["mic", "file", "youtube"]:
        return False, f"Invalid input_type: {input_type}"
    
    if export_format.lower() not in ["pdf", "word", "json"]:
        return False, f"Invalid export_format: {export_format}"
    
    return True, None

# ==================== API Routes ====================

@app.route('/summarize', methods=['POST'])
def summarize_lecture():
    """
    Main endpoint for lecture summarization
    
    Accepts:
        - input_type: "mic", "file", or "youtube"
        - export_format: "pdf", "word", or "json"
        - file: Audio/video file (for file input)
        - youtube_url: YouTube URL (for youtube input)
        - duration: Recording duration in seconds (for mic input)
        
    Returns:
        JSON response with summary data or error message
    """
    try:
        # Validate request data
        is_valid, error_msg = validate_request_data(request.form)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        input_type = request.form.get("input_type")
        export_format = request.form.get("export_format")
        
        # Process based on input type
        if input_type == "file":
            result = handle_file_upload(export_format)
        elif input_type == "youtube":
            result = handle_youtube_url(export_format)
        elif input_type == "mic":
            result = handle_microphone_input(export_format)
        else:
            return jsonify({"error": "Invalid input type"}), 400
        
        # Check for processing errors
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        app.logger.error(f"Unexpected error in summarize_lecture: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

def handle_file_upload(export_format):
    """
    Handle file upload processing
    
    Args:
        export_format (str): Desired export format
        
    Returns:
        dict: Processing result
    """
    if 'file' not in request.files:
        return {"error": "No file provided"}
    
    file = request.files['file']
    
    if file.filename == '':
        return {"error": "Empty filename"}
    
    if not allowed_file(file.filename):
        return {"error": f"File type not allowed. Supported: {', '.join(ALLOWED_EXTENSIONS)}"}
    
    # Save uploaded file securely
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        # Process the file
        result = process_lecture_input(
            source_type="file",
            file_path=filepath,
            export_format=export_format
        )
        return result
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

def handle_youtube_url(export_format):
    """
    Handle YouTube URL processing
    
    Args:
        export_format (str): Desired export format
        
    Returns:
        dict: Processing result
    """
    youtube_url = request.form.get("youtube_url", "").strip()
    
    if not youtube_url:
        return {"error": "YouTube URL is required"}
    
    # Basic URL validation
    if not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
        return {"error": "Invalid YouTube URL"}
    
    result = process_lecture_input(
        source_type="youtube",
        youtube_url=youtube_url,
        export_format=export_format
    )
    return result

def handle_microphone_input(export_format):
    """
    Handle microphone recording processing
    
    Args:
        export_format (str): Desired export format
        
    Returns:
        dict: Processing result
    """
    try:
        duration = int(request.form.get("duration", 60))
        
        # Validate duration
        if duration < 1 or duration > 600:  # Max 10 minutes
            return {"error": "Duration must be between 1 and 600 seconds"}
        
        result = process_lecture_input(
            source_type="mic",
            duration=duration,
            export_format=export_format
        )
        return result
        
    except ValueError:
        return {"error": "Invalid duration value"}

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with server status
    """
    return jsonify({
        "status": "healthy",
        "service": "AI Lecture Summarizer API"
    }), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

# ==================== Application Entry Point ====================

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
