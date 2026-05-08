"""
AI Lecture Summarizer - Core Summarization Service
Handles audio transcription, text summarization, and export functionality
"""

import os
import json
import subprocess
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from fpdf import FPDF
from docx import Document
import yt_dlp

# ==================== Configuration ====================

# Audio recording settings
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_DTYPE = 'float32'

# AI Model configuration
WHISPER_MODEL = "medium"
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"

# Text processing settings
MAX_CHUNK_WORDS = 1000
SUMMARY_MAX_LENGTH = 350
SUMMARY_MIN_LENGTH = 30
KEYPOINTS_MAX_LENGTH = 400
KEYPOINTS_MIN_LENGTH = 50

# Initialize summarization pipeline (lazy loading)
summarizer = None

def get_summarizer():
    """Lazy load the summarization pipeline"""
    global summarizer
    if summarizer is None:
        from transformers import BartForConditionalGeneration, BartTokenizer
        tokenizer = BartTokenizer.from_pretrained(SUMMARIZATION_MODEL)
        model = BartForConditionalGeneration.from_pretrained(SUMMARIZATION_MODEL)
        summarizer = (model, tokenizer)
    return summarizer

# ==================== Audio Recording ====================

def record_audio_from_microphone(duration=60, output_filename="recording.wav"):
    """
    Record audio from system microphone
    
    Args:
        duration (int): Recording duration in seconds
        output_filename (str): Output file path
        
    Returns:
        str: Path to saved audio file or None on error
    """
    print(f"🎙️ Recording audio for {duration} seconds...")
    
    try:
        # Record audio
        audio_data = sd.rec(
            int(duration * AUDIO_SAMPLE_RATE),
            samplerate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
            dtype=AUDIO_DTYPE
        )
        sd.wait()
        
        # Convert to 16-bit PCM and save
        audio_int16 = (audio_data * 32767).astype('int16')
        write(output_filename, AUDIO_SAMPLE_RATE, audio_int16)
        
        print(f"✅ Recording saved: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"❌ Recording error: {str(e)}")
        return None

# ==================== Transcription ====================

def transcribe_audio_file(file_path):
    """
    Transcribe audio file to text using Whisper
    
    Args:
        file_path (str): Path to audio/video file
        
    Returns:
        str: Transcribed text
        
    Raises:
        RuntimeError: If transcription fails
    """
    try:
        print(f"🎧 Transcribing audio: {file_path}")
        
        # Check if file is a video format that might need FFmpeg
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in video_extensions and not check_ffmpeg_installed():
            raise RuntimeError(
                f"FFmpeg is not installed. FFmpeg is required for video file processing ({file_ext} files). "
                "Please install FFmpeg from https://ffmpeg.org/download.html or use "
                "'choco install ffmpeg' (Chocolatey) or 'scoop install ffmpeg' (Scoop). "
                "Alternatively, extract the audio to MP3 or WAV format first."
            )
        
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(file_path)
        print("✅ Transcription complete")
        return result["text"]
        
    except RuntimeError:
        raise
    except Exception as e:
        error_msg = str(e)
        if 'ffmpeg' in error_msg.lower() or 'ffprobe' in error_msg.lower():
            raise RuntimeError(
                "FFmpeg error: FFmpeg is required for this file format. "
                "Please install FFmpeg from https://ffmpeg.org/download.html"
            )
        raise RuntimeError(f"Transcription failed: {error_msg}")

def check_ffmpeg_installed():
    """
    Check if FFmpeg is installed and available
    
    Returns:
        bool: True if FFmpeg is available
    """
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_and_transcribe_youtube(youtube_url):
    """
    Download YouTube video audio and transcribe
    
    Args:
        youtube_url (str): YouTube video URL
        
    Returns:
        tuple: (transcribed_text, temp_audio_file_path)
        
    Raises:
        RuntimeError: If download or transcription fails
    """
    try:
        # Check if FFmpeg is installed
        if not check_ffmpeg_installed():
            raise RuntimeError(
                "FFmpeg is not installed. FFmpeg is required for YouTube video processing. "
                "Please install FFmpeg from https://ffmpeg.org/download.html or use "
                "'choco install ffmpeg' (Chocolatey) or 'scoop install ffmpeg' (Scoop)."
            )
        
        print(f"⬇️ Downloading YouTube audio: {youtube_url}")
        
        # Configure download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'youtube_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)
            # Handle various audio formats
            audio_file = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
        
        print(f"✅ Audio downloaded: {audio_file}")
        
        # Transcribe the downloaded audio
        transcript = transcribe_audio_file(audio_file)
        return transcript, audio_file
        
    except RuntimeError:
        raise
    except Exception as e:
        error_msg = str(e)
        if 'ffmpeg' in error_msg.lower() or 'ffprobe' in error_msg.lower():
            raise RuntimeError(
                "FFmpeg error: FFmpeg is required but not properly installed. "
                "Please install FFmpeg from https://ffmpeg.org/download.html"
            )
        raise RuntimeError(f"YouTube processing failed: {error_msg}")

# ==================== Text Processing ====================

def chunk_text(text, max_words=MAX_CHUNK_WORDS):
    """
    Split text into manageable chunks for processing
    
    Args:
        text (str): Input text to chunk
        max_words (int): Maximum words per chunk
        
    Returns:
        list: List of text chunks
    """
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence_words = len(sentence.split())
        current_words = len(current_chunk.split())
        
        if current_words + sentence_words < max_words:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_summary(text):
    """
    Generate comprehensive summary from text
    
    Args:
        text (str): Input text to summarize
        
    Returns:
        str: Generated summary
    """
    print("📝 Generating summary...")
    model, tokenizer = get_summarizer()
    chunks = chunk_text(text)
    summaries = []
    
    for chunk in chunks:
        inputs = tokenizer([chunk], max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=SUMMARY_MAX_LENGTH,
            min_length=SUMMARY_MIN_LENGTH,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    
    return "\n\n".join(summaries)

def extract_key_points(text):
    """
    Extract key points from text
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Extracted key points
    """
    print("📌 Extracting key points...")
    model, tokenizer = get_summarizer()
    prompt = "Extract the main key points from this text:\n\n" + text
    chunks = chunk_text(prompt)
    keypoints = []
    
    for chunk in chunks:
        inputs = tokenizer([chunk], max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=KEYPOINTS_MAX_LENGTH,
            min_length=KEYPOINTS_MIN_LENGTH,
            num_beams=4,
            early_stopping=True
        )
        points = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        keypoints.append(points)
    
    return "\n\n".join(keypoints)

# ==================== Export Functions ====================

def export_to_pdf(summary, overview, keypoints, output_file="lecture_summary.pdf"):
    """
    Export summary to PDF format
    
    Args:
        summary (str): Overall summary
        overview (str): Brief overview
        keypoints (str): Key points
        output_file (str): Output file path
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Lecture Summary Report", ln=True, align='C')
    pdf.ln(10)
    
    # Overall Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Overall Summary", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, summary)
    pdf.ln(5)
    
    # Overview
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Overview", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, overview)
    pdf.ln(5)
    
    # Key Points
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Key Points", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, keypoints)
    
    pdf.output(output_file)
    print(f"✅ PDF exported: {output_file}")

def export_to_word(summary, overview, keypoints, output_file="lecture_summary.docx"):
    """
    Export summary to Word document format
    
    Args:
        summary (str): Overall summary
        overview (str): Brief overview
        keypoints (str): Key points
        output_file (str): Output file path
    """
    doc = Document()
    doc.add_heading("Lecture Summary Report", 0)
    
    # Overall Summary
    doc.add_heading("Overall Summary", level=1)
    doc.add_paragraph(summary)
    
    # Overview
    doc.add_heading("Overview", level=1)
    doc.add_paragraph(overview)
    
    # Key Points
    doc.add_heading("Key Points", level=1)
    doc.add_paragraph(keypoints)
    
    doc.save(output_file)
    print(f"✅ Word document exported: {output_file}")

def export_to_json(summary, overview, keypoints, output_file="lecture_summary.json"):
    """
    Export summary to JSON format
    
    Args:
        summary (str): Overall summary
        overview (str): Brief overview
        keypoints (str): Key points
        output_file (str): Output file path
    """
    data = {
        "overall_summary": summary,
        "overview": overview,
        "key_points": keypoints
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON exported: {output_file}")

# ==================== Main Processing Function ====================

def process_lecture_input(source_type, file_path=None, youtube_url=None, 
                         duration=60, export_format="pdf"):
    """
    Main function to process lecture input and generate summary
    
    Args:
        source_type (str): Input source type ("mic", "file", or "youtube")
        file_path (str): Path to audio/video file (for "file" type)
        youtube_url (str): YouTube URL (for "youtube" type)
        duration (int): Recording duration in seconds (for "mic" type)
        export_format (str): Export format ("pdf", "word", or "json")
        
    Returns:
        dict: Processing result with summary data or error message
    """
    temp_files = []
    
    try:
        # Step 1: Get transcript based on source type
        print(f"\n{'='*50}")
        print(f"Processing lecture from: {source_type}")
        print(f"{'='*50}\n")
        
        if source_type == "mic":
            audio_file = record_audio_from_microphone(duration=duration)
            if not audio_file:
                return {"error": "Failed to record audio"}
            temp_files.append(audio_file)
            transcript = transcribe_audio_file(audio_file)
            
        elif source_type == "file":
            if not file_path or not os.path.exists(file_path):
                return {"error": "Invalid or missing file path"}
            transcript = transcribe_audio_file(file_path)
            
        elif source_type == "youtube":
            if not youtube_url:
                return {"error": "YouTube URL is required"}
            transcript, temp_audio = download_and_transcribe_youtube(youtube_url)
            temp_files.append(temp_audio)
            
        else:
            return {"error": f"Invalid source type: {source_type}"}
        
        # Step 2: Generate summaries
        print("\n" + "="*50)
        print("Generating summaries...")
        print("="*50 + "\n")
        
        overall_summary = generate_summary(transcript)
        overview = generate_summary(transcript[:1000])  # First 1000 chars for overview
        keypoints = extract_key_points(transcript)
        
        # Step 3: Export to desired format
        print("\n" + "="*50)
        print(f"Exporting to {export_format.upper()}...")
        print("="*50 + "\n")
        
        export_format_lower = export_format.lower()
        
        if export_format_lower == "pdf":
            export_to_pdf(overall_summary, overview, keypoints)
            output_file = "lecture_summary.pdf"
        elif export_format_lower == "word":
            export_to_word(overall_summary, overview, keypoints)
            output_file = "lecture_summary.docx"
        elif export_format_lower == "json":
            export_to_json(overall_summary, overview, keypoints)
            output_file = "lecture_summary.json"
        else:
            return {"error": f"Unsupported export format: {export_format}"}
        
        # Step 4: Cleanup temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"🗑️ Cleaned up: {temp_file}")
        
        # Return results
        print("\n" + "="*50)
        print("✅ Processing complete!")
        print("="*50 + "\n")
        
        return {
            "overall_summary": overall_summary,
            "overview": overview,
            "keypoints": keypoints,
            "output_file": output_file
        }
        
    except Exception as e:
        # Cleanup on error
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print(f"\n❌ Error: {str(e)}\n")
        return {"error": str(e)}
