# FFmpeg Installation Guide

## Why Do You Need FFmpeg?

FFmpeg is a **free, open-source multimedia framework** that handles audio and video processing. The AI Lecture Summarizer needs FFmpeg for:

- ✅ **YouTube video downloads** - Extract audio from YouTube videos
- ✅ **Video file processing** - Process MP4, AVI, MOV, MKV, WEBM files
- ✅ **Audio format conversion** - Convert between different audio formats
- ✅ **Audio extraction** - Extract audio tracks from video files

**Without FFmpeg, you can still use:**
- ✅ Microphone recording
- ✅ MP3 audio files
- ✅ WAV audio files

---

## Installation Methods

Choose the method that works best for you:

### 🍫 Method 1: Chocolatey (Easiest - Recommended)

**What is Chocolatey?**
Chocolatey is a package manager for Windows (like apt-get for Linux).

**Step 1: Install Chocolatey (if not already installed)**

Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**Step 2: Install FFmpeg**
```powershell
choco install ffmpeg
```

**Step 3: Verify Installation**
```powershell
ffmpeg -version
```

✅ **Done!** FFmpeg is now installed and ready to use.

---

### 🪣 Method 2: Scoop (Alternative Package Manager)

**What is Scoop?**
Scoop is another package manager for Windows, focused on command-line tools.

**Step 1: Install Scoop (if not already installed)**

Open PowerShell and run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

**Step 2: Install FFmpeg**
```powershell
scoop install ffmpeg
```

**Step 3: Verify Installation**
```powershell
ffmpeg -version
```

✅ **Done!** FFmpeg is now installed and ready to use.

---

### 📥 Method 3: Manual Download (Most Control)

**Step 1: Download FFmpeg**

1. Go to: https://ffmpeg.org/download.html
2. Click on **Windows** builds
3. Recommended: https://www.gyan.dev/ffmpeg/builds/
4. Download: **ffmpeg-release-essentials.zip** (smaller) or **ffmpeg-release-full.zip** (complete)

**Step 2: Extract the Archive**

1. Extract the downloaded ZIP file to a location like:
   ```
   C:\ffmpeg
   ```
2. Inside, you'll find a folder structure like:
   ```
   C:\ffmpeg\
   ├── bin\
   │   ├── ffmpeg.exe
   │   ├── ffplay.exe
   │   └── ffprobe.exe
   ├── doc\
   └── presets\
   ```

**Step 3: Add FFmpeg to System PATH**

1. **Open System Properties:**
   - Right-click "This PC" or "My Computer"
   - Click "Properties"
   - Click "Advanced system settings"

2. **Open Environment Variables:**
   - Click "Environment Variables" button

3. **Edit PATH Variable:**
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add the path to FFmpeg's bin folder:
     ```
     C:\ffmpeg\bin
     ```
   - Click "OK" on all windows

**Step 4: Restart Terminal**

Close and reopen your terminal/command prompt for changes to take effect.

**Step 5: Verify Installation**
```cmd
ffmpeg -version
```

✅ **Done!** FFmpeg is now installed and ready to use.

---

## Verification

After installation, verify FFmpeg is working:

### Check Version
```bash
ffmpeg -version
```

**Expected output:**
```
ffmpeg version N-xxxxx-gxxxxxxx
built with gcc x.x.x
configuration: ...
```

### Check FFprobe (also installed with FFmpeg)
```bash
ffprobe -version
```

### Test FFmpeg
```bash
ffmpeg -formats
```

This should list all supported formats.

---

## Troubleshooting

### ❌ "ffmpeg is not recognized as a command"

**Cause:** FFmpeg is not in your system PATH.

**Solutions:**

1. **Restart your terminal** - PATH changes require a restart
2. **Check PATH** - Verify FFmpeg bin folder is in PATH:
   ```powershell
   $env:Path -split ';' | Select-String ffmpeg
   ```
3. **Reinstall** - Try a different installation method
4. **Use full path** - Temporarily use full path to test:
   ```cmd
   C:\ffmpeg\bin\ffmpeg.exe -version
   ```

---

### ❌ "Access Denied" during installation

**Cause:** Insufficient permissions.

**Solution:**
- Run PowerShell or Command Prompt as **Administrator**
- Right-click → "Run as administrator"

---

### ❌ Chocolatey/Scoop installation fails

**Cause:** Network issues or security policies.

**Solutions:**
1. Check your internet connection
2. Disable antivirus temporarily
3. Use manual download method instead
4. Check corporate firewall settings

---

### ❌ FFmpeg installed but app still shows error

**Cause:** Application hasn't detected FFmpeg yet.

**Solutions:**
1. **Restart the backend server:**
   - Stop the server (Ctrl+C)
   - Start again: `python api_server.py`
2. **Verify FFmpeg in terminal:**
   ```bash
   ffmpeg -version
   ```
3. **Check PATH in Python:**
   ```python
   import subprocess
   subprocess.run(['ffmpeg', '-version'])
   ```

---

## After Installation

Once FFmpeg is installed:

1. ✅ **Restart your terminal/command prompt**
2. ✅ **Verify installation:** `ffmpeg -version`
3. ✅ **Restart the backend server** (if running)
4. ✅ **Refresh the web application**
5. ✅ **Try processing a YouTube video or video file**

---

## What You Can Do Now

With FFmpeg installed, you can:

### ✅ YouTube Videos
- Paste any YouTube URL
- App downloads and extracts audio
- Transcribes and summarizes content

### ✅ Video Files
- Upload MP4, AVI, MOV, MKV, WEBM files
- App extracts audio automatically
- Processes and summarizes

### ✅ All Audio Formats
- FLAC, M4A, OGG, and more
- Automatic format conversion
- Seamless processing

---

## Quick Reference

### Installation Commands

**Chocolatey:**
```powershell
choco install ffmpeg
```

**Scoop:**
```powershell
scoop install ffmpeg
```

**Verification:**
```bash
ffmpeg -version
```

### Uninstallation

**Chocolatey:**
```powershell
choco uninstall ffmpeg
```

**Scoop:**
```powershell
scoop uninstall ffmpeg
```

**Manual:**
1. Delete the FFmpeg folder
2. Remove from PATH environment variable

---

## Additional Resources

- **Official Website:** https://ffmpeg.org/
- **Documentation:** https://ffmpeg.org/documentation.html
- **Windows Builds:** https://www.gyan.dev/ffmpeg/builds/
- **Chocolatey Package:** https://community.chocolatey.org/packages/ffmpeg
- **Scoop Package:** https://github.com/ScoopInstaller/Main/blob/master/bucket/ffmpeg.json

---

## Need Help?

If you're still having issues:

1. Check **TROUBLESHOOTING.md** for common problems
2. Verify FFmpeg version: `ffmpeg -version`
3. Check backend server logs for error messages
4. Try the manual installation method
5. Ensure your antivirus isn't blocking FFmpeg

---

## Summary

**Recommended Installation:**
1. Install Chocolatey (if not installed)
2. Run: `choco install ffmpeg`
3. Verify: `ffmpeg -version`
4. Restart backend server
5. Enjoy full functionality! 🎉

**Time Required:** 5-10 minutes
**Difficulty:** Easy
**Cost:** Free and open-source

---

**Once installed, you'll have full access to all features of the AI Lecture Summarizer!** 🚀
