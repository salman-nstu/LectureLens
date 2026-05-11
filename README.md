# LectureLens - AI-Powered Lecture Summarizer

Transcribe and summarize lectures using AI (Whisper + BART).

## Features

- 🎙️ Microphone recording
- 📂 Audio/video file upload
- 📺 YouTube video support
- 📝 AI summarization & key points extraction
- 💾 Export to PDF, Word, or JSON

## Quick Start

```bash
git clone https://github.com/salman-nstu/LectureLens.git
cd LectureLens
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python api_server.py
# In another terminal: python -m http.server 8000
```

Open `http://localhost:8000` in your browser.

## License

MIT - See [LICENSE](LICENSE) for details.

## Support

📧 salman.nstu@gmail.com  
🐛 [Issues](https://github.com/salman-nstu/LectureLens/issues)
