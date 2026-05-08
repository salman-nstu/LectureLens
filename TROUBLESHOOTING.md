# Troubleshooting Guide - AI Lecture Summarizer

## Common Errors and Solutions

### ❌ Error: "Server Error - HTTP 500" when processing video

**Cause:** FFmpeg is not installed on your system.

**What is FFmpeg?**
FFmpeg is a free, open-source tool for processing audio and video files. It's required for:
- Processing video files (MP4, AVI, MOV, MKV, WEBM)
- Downloading and converting YouTube videos
- Converting between audio formats

**Solution: Install FFmpeg**

#### Option 1: Using Chocolatey (Recommended for Windows)
```bash
choco install ffmpeg
```

#### Option 2: Using Scoop
```bash
scoop install ffmpeg
```

#### Option 3: Manual Installation
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. For Windows, use: https://www.gyan.dev/ffmpeg/builds/
3. Extract the downloaded archive
4. Add the `bin` folder to your system PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add the path to FFmpeg's `bin` folder
   - Click "OK" on all windows
5. Restart your terminal/command prompt
6. Verify installation: `ffmpeg -version`

#### Option 4: Use Audio Files Instead
If you can't install FFmpeg right now:
- ✅ Use MP3 or WAV audio files (these work without FFmpeg)
- ✅ Use microphone recording (works without FFmpeg)
- ❌ Avoid video files and YouTube URLs until FFmpeg is installed

---

### ❌ Error: "No module named 'whisper'" or similar import errors

**Cause:** Python dependencies are not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install flask flask-cors openai-whisper transformers torch yt-dlp sounddevice scipy python-docx fpdf werkzeug
```

---

### ❌ Error: "Port 5000 already in use"

**Cause:** Another application is using port 5000.

**Solution 1: Stop the conflicting process**
```bash
# Find the process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

**Solution 2: Change the port**
Edit `api_server.py` and change the port:
```python
if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,  # Changed from 5000
        debug=True
    )
```

Then access the API at `http://localhost:5001`

---

### ❌ Error: "Connection refused" when accessing frontend

**Cause:** The HTTP server is not running.

**Solution:**
```bash
python -m http.server 8000
```

Then open: http://localhost:8000

---

### ❌ Error: "File too large" when uploading

**Cause:** File exceeds the 500MB limit.

**Solution:**
- Use a smaller file
- Or edit `api_server.py` to increase `MAX_FILE_SIZE`
- Or extract just the audio portion of the video first

---

### ❌ Error: Slow processing or timeout

**Cause:** Large files or slow hardware.

**Solutions:**
1. **Use a smaller Whisper model** (faster but less accurate):
   - Edit `summarization_service.py`
   - Change `WHISPER_MODEL = "medium"` to `WHISPER_MODEL = "base"` or `"tiny"`

2. **Process shorter segments**:
   - Split long videos into smaller chunks
   - Process each chunk separately

3. **Use GPU acceleration** (if you have an NVIDIA GPU):
   - Install CUDA toolkit
   - Install PyTorch with CUDA support
   - Whisper will automatically use GPU

---

### ❌ Error: "Out of memory"

**Cause:** Not enough RAM for large files or models.

**Solutions:**
1. Use a smaller Whisper model (`tiny` or `base`)
2. Close other applications to free up memory
3. Process smaller files
4. Restart the server to clear memory

---

### ❌ Error: Models downloading slowly

**Cause:** First-time model downloads from Hugging Face.

**What's happening:**
- Whisper model: ~1.5 GB (one-time download)
- BART summarization model: ~1.6 GB (one-time download)
- Total: ~3 GB of AI models

**Solution:**
- Be patient - this only happens once
- Models are cached locally for future use
- Check download progress in the server logs

---

### ❌ Error: "YouTube download failed"

**Possible causes and solutions:**

1. **FFmpeg not installed**
   - See FFmpeg installation instructions above

2. **Invalid YouTube URL**
   - Make sure the URL is correct
   - Use the full URL: `https://www.youtube.com/watch?v=VIDEO_ID`
   - Or short URL: `https://youtu.be/VIDEO_ID`

3. **Video is private or restricted**
   - The video must be publicly accessible
   - Age-restricted videos may not work

4. **Network issues**
   - Check your internet connection
   - Try again later

---

### ❌ Error: "Microphone not working"

**Possible causes and solutions:**

1. **No microphone connected**
   - Connect a microphone or use your device's built-in mic
   - Check Windows sound settings

2. **Permission denied**
   - Allow microphone access in Windows settings
   - Settings → Privacy → Microphone

3. **Wrong audio device**
   - Check which microphone is set as default
   - Settings → System → Sound → Input

---

## Verification Checklist

Before reporting an issue, verify:

- [ ] Python 3.8+ is installed: `python --version`
- [ ] All dependencies are installed: `pip list`
- [ ] Backend server is running: http://localhost:5000/health
- [ ] Frontend server is running: http://localhost:8000
- [ ] FFmpeg is installed (for video/YouTube): `ffmpeg -version`
- [ ] Firewall is not blocking ports 5000 or 8000
- [ ] Sufficient disk space for model downloads (~3 GB)
- [ ] Sufficient RAM (at least 4 GB recommended)

---

## Getting Help

If you're still experiencing issues:

1. **Check the server logs**
   - Look at the terminal where `python api_server.py` is running
   - Error messages will appear there

2. **Check browser console**
   - Press F12 in your browser
   - Look for errors in the Console tab

3. **Try a simple test**
   - Use microphone recording with a 10-second duration
   - This tests the basic functionality

4. **Restart everything**
   ```bash
   # Stop both servers (Ctrl+C)
   # Then restart:
   python api_server.py
   # In another terminal:
   python -m http.server 8000
   ```

---

## Performance Tips

### For faster processing:

1. **Use smaller Whisper models**
   - `tiny`: Fastest, least accurate
   - `base`: Fast, decent accuracy
   - `small`: Balanced
   - `medium`: Slower, better accuracy (default)
   - `large`: Slowest, best accuracy

2. **Use GPU if available**
   - Install CUDA and PyTorch with CUDA support
   - Significant speed improvement

3. **Process shorter content**
   - Break long videos into segments
   - Process each segment separately

4. **Close unnecessary applications**
   - Free up RAM and CPU resources

---

## File Format Support

### ✅ Works WITHOUT FFmpeg:
- MP3 audio files
- WAV audio files
- Microphone recording

### ⚠️ Requires FFmpeg:
- MP4 video files
- AVI video files
- MOV video files
- MKV video files
- WEBM video files
- YouTube URLs
- FLAC audio files
- M4A audio files

---

## Quick Reference

### Start the application:
```bash
# Terminal 1 - Backend
python api_server.py

# Terminal 2 - Frontend
python -m http.server 8000
```

### Access URLs:
- Frontend: http://localhost:8000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health

### Install FFmpeg:
```bash
# Chocolatey
choco install ffmpeg

# Scoop
scoop install ffmpeg

# Manual
# Download from https://ffmpeg.org/download.html
```

---

**Still having issues? Check the server logs for detailed error messages!**
