# LectureLens - AI-Powered Lecture Summarizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional web application that uses cutting-edge AI to transcribe and summarize lectures from multiple sources. Built with OpenAI's Whisper for transcription and Facebook's BART for intelligent summarization.

![LectureLens Demo](https://via.placeholder.com/800x400?text=LectureLens+Demo)

---

## ✨ Features

### 🎯 Core Functionality
- **🎙️ Real-time Microphone Recording** - Record lectures directly with visual feedback
- **📂 File Upload Support** - Process audio/video files (MP3, MP4, WAV, AVI, MOV, FLAC, M4A, WEBM)
- **📺 YouTube Integration** - Extract and summarize YouTube videos
- **🤖 AI-Powered Transcription** - OpenAI Whisper for accurate speech-to-text
- **📝 Intelligent Summarization** - Facebook BART for concise summaries
- **🔑 Key Points Extraction** - Automatic identification of main topics

### 💾 Export Options
- **PDF Documents** - Professional formatted reports
- **Word Documents (.docx)** - Editable summaries
- **JSON Format** - Structured data for integration

### 🎨 User Experience
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark/Light Theme** - Toggle between themes with persistent preference
- **Real-time Feedback** - Visual recording indicator with timer
- **Progress Tracking** - Status updates during processing
- **Clean Interface** - Modern, intuitive design

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **FFmpeg** - For audio/video processing (see installation below)
- **Git** - For cloning the repository

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/salman-nstu/LectureLens.git
cd LectureLens
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First-time installation will download AI models (~3GB). This may take several minutes.

#### 4. Install FFmpeg

FFmpeg is required for video processing and YouTube downloads.

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Scoop):**
```bash
scoop install ffmpeg
```

**Windows (Manual):**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

---

## 📖 Usage

### Starting the Application

#### 1. Start Backend Server

```bash
python api_server.py
```

Server will start at: `http://127.0.0.1:5000`

#### 2. Start Frontend Server

```bash
python -m http.server 8000
```

Frontend will be available at: `http://localhost:8000`

### Using the Application

1. **Open Browser** - Navigate to `http://localhost:8000`
2. **Select Input Source**:
   - 🎙️ **Microphone** - Record live audio (choose duration: 30s to 5min)
   - 📂 **File Upload** - Upload audio/video files
   - 📺 **YouTube URL** - Paste YouTube video link
3. **Choose Export Format** - PDF, Word, or JSON
4. **Process** - Click play button to start
5. **View Results** - Summary displayed with download option

### What Works Without FFmpeg

✅ **Microphone recording**  
✅ **MP3 audio files**  
✅ **WAV audio files**

### What Requires FFmpeg

⚠️ **YouTube videos**  
⚠️ **Video files** (MP4, AVI, MOV, MKV, WEBM)  
⚠️ **Some audio formats** (FLAC, M4A)

---

## 🏗️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Variables
- **JavaScript (ES6+)** - Async/await, modules
- **Material Symbols** - Icon library

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0+** - Web framework
- **Flask-CORS** - Cross-origin resource sharing

### AI/ML Models
- **OpenAI Whisper** - Speech-to-text transcription
  - Model: Medium (1.5GB)
  - Accuracy: High
  - Languages: 99+ supported
- **Facebook BART** - Text summarization
  - Model: bart-large-cnn (1.63GB)
  - Task: Abstractive summarization
  - Performance: State-of-the-art

### Libraries & Tools
- **yt-dlp** - YouTube video/audio extraction
- **sounddevice** - Audio recording
- **scipy** - Scientific computing for audio
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face model library
- **python-docx** - Word document generation
- **fpdf** - PDF generation

---

## 📁 Project Structure

```
LectureLens/
├── 📄 index.html                  # Main HTML interface
├── 🎨 styles.css                  # Application styles & themes
├── ⚡ app.js                      # Frontend JavaScript logic
├── 🔧 api_server.py              # Flask API server
├── 🤖 summarization_service.py   # AI processing service
├── ⚙️ config.py                  # Configuration settings
├── 🖼️ logo.svg                   # Application logo
├── 📦 requirements.txt           # Python dependencies
├── 🚫 .gitignore                 # Git ignore rules
├── 📖 README.md                  # Documentation
├── 📜 LICENSE                    # License file
└── 📁 videos/                    # Background video assets
    └── desktop-video.mp4
```

---

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Lecture Summarizer API"
}
```

#### Process Lecture
```http
POST /summarize
Content-Type: multipart/form-data
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input_type` | string | Yes | Input source: `mic`, `file`, or `youtube` |
| `export_format` | string | Yes | Export format: `pdf`, `word`, or `json` |
| `file` | file | Conditional | Audio/video file (required for `file` type) |
| `youtube_url` | string | Conditional | YouTube URL (required for `youtube` type) |
| `duration` | integer | Optional | Recording duration in seconds (for `mic` type, default: 60) |

**Success Response (200):**
```json
{
  "overall_summary": "Comprehensive summary of the lecture...",
  "overview": "Brief overview of main topics...",
  "keypoints": "Key points extracted from content...",
  "output_file": "lecture_summary.pdf"
}
```

**Error Response (400/500):**
```json
{
  "error": "Error message describing what went wrong"
}
```

### Example Requests

**Microphone Recording:**
```javascript
const formData = new FormData();
formData.append('input_type', 'mic');
formData.append('export_format', 'pdf');
formData.append('duration', '60');

fetch('http://127.0.0.1:5000/summarize', {
  method: 'POST',
  body: formData
});
```

**File Upload:**
```javascript
const formData = new FormData();
formData.append('input_type', 'file');
formData.append('export_format', 'word');
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:5000/summarize', {
  method: 'POST',
  body: formData
});
```

**YouTube URL:**
```javascript
const formData = new FormData();
formData.append('input_type', 'youtube');
formData.append('export_format', 'json');
formData.append('youtube_url', 'https://www.youtube.com/watch?v=...');

fetch('http://127.0.0.1:5000/summarize', {
  method: 'POST',
  body: formData
});
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional) for custom configuration:

```env
FLASK_ENV=development
FLASK_DEBUG=True
HOST=127.0.0.1
PORT=5000
MAX_FILE_SIZE=524288000
```

### Backend Configuration

Edit `config.py` to customize settings:

```python
# Server Settings
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

# File Upload Settings
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'avi', 'mov', 'flac', 'm4a', 'webm'}

# AI Model Settings
WHISPER_MODEL = "medium"  # Options: tiny, base, small, medium, large
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"

# Text Processing Settings
MAX_CHUNK_WORDS = 1000
SUMMARY_MAX_LENGTH = 350
SUMMARY_MIN_LENGTH = 30
KEYPOINTS_MAX_LENGTH = 400
KEYPOINTS_MIN_LENGTH = 50
```

### Model Selection Guide

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `tiny` | 39M | Very Fast | Low | Quick testing |
| `base` | 74M | Fast | Medium | General use |
| `small` | 244M | Moderate | Good | Balanced |
| `medium` | 769M | Slow | High | **Recommended** |
| `large` | 1550M | Very Slow | Highest | Maximum accuracy |

### Frontend Configuration

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

## 🎯 Performance Optimization

### For Faster Processing

1. **Use Smaller Whisper Model**
```python
WHISPER_MODEL = "base"  # Faster, less accurate
```

2. **Reduce Summary Length**
```python
SUMMARY_MAX_LENGTH = 200
SUMMARY_MIN_LENGTH = 50
```

3. **Enable GPU Acceleration** (if available)
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### For Better Accuracy

1. **Use Larger Whisper Model**
```python
WHISPER_MODEL = "large"  # Slower, more accurate
```

2. **Increase Summary Detail**
```python
SUMMARY_MAX_LENGTH = 500
SUMMARY_MIN_LENGTH = 100
```

### Processing Time Estimates

| Input Length | Whisper (medium) | Summarization | Total |
|--------------|------------------|---------------|-------|
| 1 minute | ~10 seconds | ~5 seconds | ~15 seconds |
| 5 minutes | ~50 seconds | ~10 seconds | ~1 minute |
| 10 minutes | ~1.5 minutes | ~15 seconds | ~2 minutes |
| 30 minutes | ~5 minutes | ~30 seconds | ~5.5 minutes |

*Times are approximate and vary based on hardware*

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Module Not Found Errors

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. FFmpeg Not Found

**Problem:** `FFmpeg is not installed` error when processing videos

**Solution:**
```bash
# Install FFmpeg (see installation section)
# Verify installation:
ffmpeg -version

# Restart backend server after installation
```

#### 3. Port Already in Use

**Problem:** `Address already in use` error

**Solution:**
```bash
# Option 1: Kill process using port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Option 2: Change port in config.py
PORT = 5001
```

#### 4. CORS Errors

**Problem:** CORS policy blocking requests

**Solution:**
```bash
# Ensure Flask-CORS is installed
pip install flask-cors

# Verify CORS is enabled in api_server.py
```

#### 5. Microphone Not Working

**Problem:** No audio captured from microphone

**Solution:**
- Check browser permissions (allow microphone access)
- Verify microphone is connected and working
- Check system audio settings
- Try different browser

#### 6. Large File Upload Fails

**Problem:** File upload fails for large files

**Solution:**
```python
# Increase MAX_FILE_SIZE in config.py
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB
```

#### 7. Slow Processing

**Problem:** Processing takes too long

**Solution:**
```python
# Use smaller Whisper model
WHISPER_MODEL = "base"  # or "tiny"

# Or enable GPU acceleration (if available)
```

#### 8. Out of Memory

**Problem:** System runs out of memory

**Solution:**
- Use smaller Whisper model
- Process shorter audio segments
- Close other applications
- Increase system RAM

---

## 🚀 Deployment

### Production Deployment

#### 1. Security Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for sensitive data
- [ ] Implement authentication/authorization
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Validate and sanitize all inputs
- [ ] Set up CORS properly
- [ ] Use secure session management

#### 2. Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app

# With timeout for long-running requests
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 api_server:app
```

#### 3. Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "300", "api_server:app"]
```

Build and run:
```bash
docker build -t lecturelens .
docker run -p 5000:5000 lecturelens
```

#### 4. Cloud Deployment Options

- **Heroku** - Easy deployment with buildpacks
- **AWS EC2** - Full control, scalable
- **Google Cloud Run** - Serverless containers
- **Azure App Service** - Managed platform
- **DigitalOcean** - Simple VPS hosting

### Environment-Specific Settings

**Development:**
```python
DEBUG = True
HOST = "127.0.0.1"
```

**Production:**
```python
DEBUG = False
HOST = "0.0.0.0"
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

### Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/LectureLens.git
cd LectureLens
```

3. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

4. Make your changes and commit:
```bash
git add .
git commit -m "Add: your feature description"
```

5. Push to your fork:
```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request

### Code Style Guidelines

**Python:**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

**JavaScript:**
- Use ES6+ features
- Use meaningful variable names
- Add JSDoc comments for functions
- Follow consistent formatting

**Commit Messages:**
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues when applicable

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For the Whisper speech recognition model
- **Facebook AI** - For the BART summarization model
- **Hugging Face** - For the Transformers library
- **Flask Team** - For the excellent web framework
- **Contributors** - For all improvements and bug fixes

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/salman-nstu/LectureLens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/salman-nstu/LectureLens/discussions)
- **Email**: salman.nstu@gmail.com

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Multi-language support (Spanish, French, German, etc.)
- [ ] Real-time transcription display
- [ ] Speaker diarization (identify different speakers)
- [ ] Custom summarization templates
- [ ] Cloud storage integration (AWS S3, Google Drive)

### Version 2.1 (Future)
- [ ] User authentication system
- [ ] Batch processing for multiple files
- [ ] Mobile app (React Native)
- [ ] API rate limiting and quotas
- [ ] Comprehensive logging and monitoring
- [ ] Webhook support for integrations

### Version 3.0 (Long-term)
- [ ] Live streaming transcription
- [ ] Collaborative editing of summaries
- [ ] Integration with LMS platforms
- [ ] Advanced analytics dashboard
- [ ] Custom AI model training

---

## 📊 System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Storage**: 5GB free space
- **OS**: Windows 10, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8+
- **Internet**: Required for model downloads

### Recommended Requirements
- **CPU**: Quad-core processor or better
- **RAM**: 8GB or more
- **Storage**: 10GB free space (SSD recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)
- **Internet**: Broadband connection

---

## 🔒 Security

### Reporting Security Issues

If you discover a security vulnerability, please email salman.nstu@gmail.com instead of using the issue tracker.

### Security Best Practices

- Keep dependencies up to date
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting
- Validate all user inputs
- Use secure session management

---

## 📈 Performance Metrics

### Model Performance

**Whisper (Medium):**
- Word Error Rate (WER): ~5-10%
- Languages: 99+ supported
- Real-time factor: 0.5-1.0x

**BART (Large-CNN):**
- ROUGE-1: 44.16
- ROUGE-2: 21.28
- ROUGE-L: 40.90

### API Performance

- Health check: < 10ms
- File validation: < 50ms
- Transcription: ~0.5-1.0x real-time
- Summarization: ~5-10 seconds per 1000 words

---

## 🎓 Use Cases

- **Students** - Summarize lecture recordings
- **Researchers** - Process interview transcripts
- **Journalists** - Transcribe and summarize interviews
- **Content Creators** - Generate video summaries
- **Businesses** - Meeting notes and summaries
- **Educators** - Create study materials

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

## 📚 Additional Resources

- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

---

<div align="center">

**Built with ❤️ using modern AI and web technologies**

[⬆ Back to Top](#lecturelens---ai-powered-lecture-summarizer)

</div>
