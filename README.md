# LectureLens - AI-Powered Lecture Summarizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered web application that transcribes and summarizes lectures from multiple sources using OpenAI's Whisper and Facebook's BART.

## ✨ Features

- **🎙️ Microphone Recording** - Record lectures directly
- **📂 File Upload** - Process audio/video files (MP3, MP4, WAV, AVI, MOV, FLAC, M4A, WEBM)
- **📺 YouTube Integration** - Extract and summarize YouTube videos
- **🤖 AI Transcription** - OpenAI Whisper for accurate speech-to-text
- **📝 Intelligent Summarization** - Facebook BART for concise summaries
- **💾 Export Options** - PDF, Word, or JSON formats
- **🎨 Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (included with Python)
- FFmpeg (for video processing)

### Installation

```bash
# Clone repository
git clone https://github.com/salman-nstu/LectureLens.git
cd LectureLens

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Terminal 1: Start backend
python api_server.py

# Terminal 2: Start frontend
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## 🏗️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.8+, Flask
- **AI Models**: OpenAI Whisper (transcription), Facebook BART (summarization)
- **Key Libraries**: yt-dlp, sounddevice, PyTorch, Transformers, python-docx, fpdf

## 📁 Project Structure

```
LectureLens/
├── index.html              # Main HTML interface
├── styles.css              # Application styles
├── app.js                  # Frontend JavaScript
├── api_server.py           # Flask API server
├── summarization_service.py # AI processing service
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── LICENSE                 # License file
├── README.md               # Documentation
└── videos/                 # Video assets
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
HOST = "127.0.0.1"
PORT = 5000
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
WHISPER_MODEL = "medium"           # Options: tiny, base, small, medium, large
SUMMARY_MAX_LENGTH = 350
SUMMARY_MIN_LENGTH = 30
```

## 🐛 Troubleshooting

**Module not found errors:**
```bash
pip install -r requirements.txt
```

**FFmpeg not found:**
Install FFmpeg using:
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**Port already in use:**
```bash
# Change port in config.py
PORT = 5001
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI (Whisper model)
- Facebook AI (BART model)
- Hugging Face (Transformers library)
- Flask team

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/salman-nstu/LectureLens/issues)
- **Email**: salman.nstu@gmail.com
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
