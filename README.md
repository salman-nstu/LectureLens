# AI-Powered Lecture Summarizer

A professional web application that uses AI to transcribe and summarize lectures from multiple sources including microphone input, file uploads, and YouTube videos. Built with OpenAI's Whisper for transcription and transformer models for intelligent summarization.

---

## Features

- **Multiple Input Sources**
  - 🎙️ Real-time microphone recording
  - 📂 Audio/video file upload (MP3, MP4, WAV, etc.)
  - 📺 YouTube URL processing

- **AI-Powered Processing**
  - Automatic speech-to-text transcription using Whisper
  - Intelligent text summarization with FLAN-T5
  - Key points extraction

- **Flexible Export Options**
  - PDF documents
  - Word documents (.docx)
  - JSON format

- **Modern UI/UX**
  - Responsive design for all devices
  - Dark/Light theme toggle
  - Real-time processing feedback
  - Clean, professional interface

---

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Material Symbols Icons
- Responsive design with CSS Variables

### Backend
- Python 3.8+
- Flask (Web framework)
- Flask-CORS (Cross-origin resource sharing)

### AI/ML
- OpenAI Whisper (Speech recognition)
- Transformers (NLP models)
- Google FLAN-T5 Large (Summarization)

### Additional Libraries
- yt-dlp (YouTube audio extraction)
- sounddevice (Audio recording)
- scipy (Audio processing)
- python-docx (Word generation)
- fpdf (PDF generation)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (for audio processing)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd lecture-summarizer
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## Usage

### Starting the Application

1. **Start the Backend Server**

```bash
python api_server.py
```

The server will start at `http://127.0.0.1:5000`

2. **Open the Frontend**

Open `index.html` in your web browser, or use a local server:

```bash
# Using Python's built-in server
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

### Using the Application

1. **Select Input Source** - Choose from Microphone, File Upload, or YouTube URL
2. **Provide Input** - Upload file, paste URL, or use microphone
3. **Select Export Format** - Choose PDF, Word, or JSON
4. **Process** - Click the play button to start processing
5. **View Results** - Summary will be displayed and saved to file

---

## Project Structure

```
lecture-summarizer/
├── index.html                  # Main HTML interface
├── styles.css                  # Application styles
├── app.js                      # Frontend JavaScript logic
├── api_server.py              # Flask API server
├── summarization_service.py   # Core AI processing logic
├── config.py                  # Configuration settings
├── logo.svg                   # Application logo
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                  # This file
└── videos/                    # Background video assets
    └── desktop-video.mp4
```

---

## API Documentation

### Endpoints

#### `POST /summarize`

Process lecture input and generate summary.

**Request (multipart/form-data):**

```javascript
{
  "input_type": "mic" | "file" | "youtube",
  "export_format": "pdf" | "word" | "json",
  "file": File,              // Required for "file" type
  "youtube_url": string,     // Required for "youtube" type
  "duration": number         // Optional for "mic" type (default: 60)
}
```

**Response:**

```javascript
{
  "overall_summary": string,
  "overview": string,
  "keypoints": string,
  "output_file": string
}
```

**Error Response:**

```javascript
{
  "error": string
}
```

#### `GET /health`

Health check endpoint.

**Response:**

```javascript
{
  "status": "healthy",
  "service": "AI Lecture Summarizer API"
}
```

---

## Configuration

### Backend Settings

Edit `config.py` to customize:

```python
# Server settings
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

# File upload settings
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'avi', 'mov', ...}

# AI model settings
WHISPER_MODEL = "medium"  # Options: tiny, base, small, medium, large
SUMMARIZATION_MODEL = "google/flan-t5-large"

# Text processing
MAX_CHUNK_WORDS = 1000
SUMMARY_MAX_LENGTH = 350
SUMMARY_MIN_LENGTH = 30
```

### Frontend Settings

Edit `app.js` to change API endpoint:

```javascript
const API_CONFIG = {
  baseURL: "http://127.0.0.1:5000",
  endpoints: {
    summarize: "/summarize"
  }
};
```

---

## Performance Optimization

### For Faster Processing

Use a smaller Whisper model in `config.py`:

```python
WHISPER_MODEL = "base"  # Faster, less accurate
```

### For Better Accuracy

Use a larger Whisper model:

```python
WHISPER_MODEL = "large"  # Slower, more accurate
```

### Adjust Summarization Length

```python
SUMMARY_MAX_LENGTH = 200  # Shorter summaries
SUMMARY_MIN_LENGTH = 50
```

---

## Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

**Issue: FFmpeg not found**
```bash
# Solution: Install FFmpeg and add to PATH
# Verify installation:
ffmpeg -version
```

**Issue: CORS errors in browser**
```bash
# Solution: Ensure Flask-CORS is installed
pip install flask-cors
```

**Issue: Microphone not working**
- Check browser permissions for microphone access
- Ensure microphone is connected and working

**Issue: Large files failing to upload**
```python
# Solution: Increase MAX_FILE_SIZE in config.py
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB
```

**Issue: Slow processing**
```python
# Solution: Use smaller Whisper model
WHISPER_MODEL = "base"  # or "tiny"
```

**Issue: Port already in use**
```python
# Solution: Change port in config.py
PORT = 5001
```

---

## Development

### Running in Development Mode

```bash
# Backend with auto-reload
python api_server.py

# Frontend with live server
python -m http.server 8000
```

### Code Structure

- **Frontend (`app.js`)**: Event handlers, API communication, UI updates
- **API Layer (`api_server.py`)**: HTTP request handling, validation, file management
- **Service Layer (`summarization_service.py`)**: Audio processing, transcription, summarization, export

---

## Deployment

### Production Considerations

1. **Security**
   - Set `DEBUG = False` in production
   - Implement authentication
   - Add rate limiting
   - Use HTTPS

2. **Performance**
   - Use production WSGI server (Gunicorn, uWSGI)
   - Implement caching
   - Use CDN for static assets

3. **Scalability**
   - Use task queue (Celery) for async processing
   - Implement load balancing
   - Use cloud storage for files

### Example Production Setup

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### Code Style

- Python: Follow PEP 8
- JavaScript: Use ES6+ features
- Add comments for complex logic
- Write descriptive commit messages

---

## License

This project is provided as-is for educational and commercial use. Add an appropriate license file (MIT, Apache 2.0, etc.) based on your requirements.

---

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

## Future Enhancements

- [ ] Multi-language support
- [ ] Real-time transcription display
- [ ] Speaker diarization
- [ ] Custom summarization templates
- [ ] Cloud storage integration
- [ ] User authentication system
- [ ] Batch processing
- [ ] Mobile app version
- [ ] API rate limiting
- [ ] Comprehensive logging and monitoring

---

**Built with modern web technologies and AI**
