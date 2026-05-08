/**
 * AI Lecture Summarizer - Frontend Application
 * Handles user interactions, API communication, and UI updates
 */

// ==================== DOM Elements ====================
const chatsContainer = document.querySelector(".chats-container");
const promptForm = document.querySelector(".prompt-form");
const inputType = document.querySelector("#input-type");
const exportFormat = document.querySelector("#export-format");
const youtubeInput = document.querySelector("#youtube-link");
const fileInput = document.querySelector("#audio-file");
const micDuration = document.querySelector("#mic-duration");
const themeToggleBtn = document.querySelector("#theme-toggle-btn");
const deleteChatsBtn = document.querySelector("#delete-chats-btn");
const recordingModal = document.querySelector("#recording-modal");
const recordingTimer = document.querySelector("#recording-timer");
const recordingStatus = document.querySelector("#recording-status");
const stopRecordingBtn = document.querySelector("#stop-recording-btn");

// ==================== Recording State ====================
let recordingInterval = null;
let recordingStartTime = null;
let isRecording = false;
let recordingDuration = 60;

// ==================== Configuration ====================
const API_CONFIG = {
  baseURL: "http://127.0.0.1:5000",
  endpoints: {
    summarize: "/summarize"
  }
};

// ==================== Event Listeners ====================

/**
 * Handle input type changes to show/hide relevant input fields
 */
inputType.addEventListener("change", () => {
  const selectedType = inputType.value;
  youtubeInput.style.display = selectedType === "youtube" ? "block" : "none";
  fileInput.style.display = selectedType === "file" ? "block" : "none";
  micDuration.style.display = selectedType === "mic" ? "block" : "none";
});

/**
 * Handle form submission for processing lecture content
 */
promptForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await processLectureInput();
});

/**
 * Toggle between light and dark themes
 */
themeToggleBtn.addEventListener("click", () => {
  const isLightTheme = document.body.classList.toggle("light-theme");
  localStorage.setItem("themeColor", isLightTheme ? "light_mode" : "dark_mode");
  themeToggleBtn.textContent = isLightTheme ? "dark_mode" : "light_mode";
});

/**
 * Clear all chat messages and reset UI
 */
deleteChatsBtn.addEventListener("click", () => {
  chatsContainer.innerHTML = "";
  document.body.classList.remove("chats-active");
});

/**
 * Stop recording when stop button is clicked
 */
stopRecordingBtn.addEventListener("click", () => {
  stopRecording();
});

// ==================== UI Functions ====================

/**
 * Show recording modal with timer and visualizer
 */
function showRecordingModal() {
  recordingModal.style.display = "flex";
  isRecording = true;
  recordingStartTime = Date.now();
  
  // Update timer every 100ms for smooth display
  recordingInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    recordingTimer.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    // Calculate progress percentage
    const progress = (elapsed / recordingDuration) * 100;
    
    // Update status message based on progress
    if (progress < 10) {
      recordingStatus.textContent = "🎤 Listening...";
    } else if (progress < 50) {
      recordingStatus.textContent = "🎵 Recording your audio...";
    } else if (progress < 80) {
      recordingStatus.textContent = "📝 Keep speaking...";
    } else if (progress < 95) {
      recordingStatus.textContent = "⏰ Almost done...";
    } else {
      recordingStatus.textContent = "✅ Finishing up...";
    }
    
    // Auto-stop if duration exceeded (safety check)
    if (elapsed >= recordingDuration) {
      stopRecording();
      processRecordedAudio();
    }
  }, 100);
}

/**
 * Hide recording modal and stop timer
 */
function hideRecordingModal() {
  recordingModal.style.display = "none";
  isRecording = false;
  
  if (recordingInterval) {
    clearInterval(recordingInterval);
    recordingInterval = null;
  }
  
  // Reset display
  recordingTimer.textContent = "00:00";
  recordingStatus.textContent = "Listening...";
}

/**
 * Stop recording and process the audio
 */
function stopRecording() {
  if (!isRecording) return;
  
  hideRecordingModal();
  displayMessage("🔄 Processing Audio", "Transcribing and summarizing your recording...");
}

/**
 * Display a message block in the chat container
 * @param {string} title - Message title
 * @param {string} content - Message content
 * @param {string} type - Message type (default: "bot-message")
 */
function displayMessage(title, content, type = "bot-message") {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", type);
  messageDiv.innerHTML = `
    <img class="avatar" src="logo.svg" alt="AI Avatar" />
    <div class="message-text">
      <strong>${title}</strong><br><br>${content}
    </div>
  `;
  chatsContainer.appendChild(messageDiv);
  document.body.classList.add("chats-active");
  
  // Smooth scroll to new message
  setTimeout(() => {
    messageDiv.scrollIntoView({ behavior: "smooth", block: "end" });
  }, 100);
}

/**
 * Clear all messages from the chat container
 */
function clearMessages() {
  chatsContainer.innerHTML = "";
}

// ==================== Validation Functions ====================

/**
 * Validate form inputs before submission
 * @returns {Object} Validation result with isValid flag and error message
 */
function validateInputs() {
  const selectedType = inputType.value;
  const selectedFormat = exportFormat.value;
  const youtubeURL = youtubeInput.value.trim();
  const uploadedFile = fileInput.files[0];

  if (!selectedType || !selectedFormat) {
    return {
      isValid: false,
      error: "Please select both input source and export format."
    };
  }

  if (selectedType === "youtube" && !youtubeURL) {
    return {
      isValid: false,
      error: "Please enter a valid YouTube URL."
    };
  }

  if (selectedType === "file" && !uploadedFile) {
    return {
      isValid: false,
      error: "Please upload an audio or video file."
    };
  }

  return { isValid: true };
}

// ==================== API Functions ====================

/**
 * Build FormData object for API request
 * @returns {FormData} Prepared form data
 */
function buildRequestData() {
  const formData = new FormData();
  const selectedType = inputType.value;
  const selectedFormat = exportFormat.value;

  formData.append("input_type", selectedType);
  formData.append("export_format", selectedFormat);

  if (selectedType === "file") {
    formData.append("file", fileInput.files[0]);
  } else if (selectedType === "youtube") {
    formData.append("youtube_url", youtubeInput.value.trim());
  } else if (selectedType === "mic") {
    const duration = micDuration.value || "60";
    formData.append("duration", duration);
  }

  return formData;
}

/**
 * Send request to backend API
 * @param {FormData} formData - Request data
 * @returns {Promise<Object>} API response
 */
async function sendToAPI(formData) {
  const url = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.summarize}`;
  
  const response = await fetch(url, {
    method: "POST",
    body: formData
  });

  // Parse JSON response
  const data = await response.json();

  // If response is not OK, throw error with backend message
  if (!response.ok) {
    const errorMessage = data.error || `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }

  return data;
}

/**
 * Display API response in the UI
 * @param {Object} data - Response data from API
 */
function displayResults(data) {
  clearMessages();

  if (data.error) {
    displayMessage("❌ Error", data.error);
    return;
  }

  displayMessage("📜 Overall Summary", data.overall_summary);
  displayMessage("📄 Overview", data.overview);
  displayMessage("📌 Key Points", data.keypoints);
  displayMessage("⬇️ Export", `File saved as: <code>${data.output_file}</code>`);
}

// ==================== Main Processing Function ====================

/**
 * Process lecture input and display results
 */
async function processLectureInput() {
  // Validate inputs
  const validation = validateInputs();
  if (!validation.isValid) {
    alert(validation.error);
    return;
  }

  const selectedType = inputType.value;

  // Show recording modal for microphone input
  if (selectedType === "mic") {
    recordingDuration = parseInt(micDuration.value) || 60;
    showRecordingModal();
    
    // Auto-stop after selected duration
    setTimeout(() => {
      if (isRecording) {
        stopRecording();
        processRecordedAudio();
      }
    }, recordingDuration * 1000);
    
    return; // Don't process immediately, wait for recording to finish
  }

  // For file and YouTube, process immediately
  await processInput();
}

/**
 * Process the recorded audio after recording stops
 */
async function processRecordedAudio() {
  await processInput();
}

/**
 * Main processing function for all input types
 */
async function processInput() {
  // Clear previous results and show loading
  clearMessages();
  displayMessage("🔄 Processing Input", "Please wait while we process your request...");

  try {
    // Build request and send to API
    const formData = buildRequestData();
    const responseData = await sendToAPI(formData);

    // Display results
    displayResults(responseData);

  } catch (error) {
    clearMessages();
    
    // Check if it's an FFmpeg error
    const errorMsg = error.message || "Unknown error occurred";
    const isFFmpegError = errorMsg.toLowerCase().includes('ffmpeg');
    
    if (isFFmpegError) {
      // Show detailed FFmpeg installation instructions
      displayMessage(
        "⚠️ FFmpeg Required",
        `<strong>FFmpeg is not installed on your system.</strong><br><br>
        FFmpeg is required for:<br>
        • YouTube video downloads<br>
        • Video file processing (MP4, AVI, MOV, etc.)<br>
        • Some audio format conversions<br><br>
        <strong>How to install FFmpeg:</strong><br><br>
        <strong>Option 1: Chocolatey</strong><br>
        <code>choco install ffmpeg</code><br><br>
        <strong>Option 2: Scoop</strong><br>
        <code>scoop install ffmpeg</code><br><br>
        <strong>Option 3: Manual Download</strong><br>
        Visit: <a href="https://ffmpeg.org/download.html" target="_blank">https://ffmpeg.org/download.html</a><br><br>
        <strong>After installation:</strong><br>
        1. Restart your terminal/command prompt<br>
        2. Verify: <code>ffmpeg -version</code><br>
        3. Refresh this page<br>
        4. Try again!<br><br>
        <strong>What works WITHOUT FFmpeg:</strong><br>
        ✅ Microphone recording<br>
        ✅ MP3 audio files<br>
        ✅ WAV audio files<br><br>
        See <strong>TROUBLESHOOTING.md</strong> for detailed help.`
      );
    } else {
      // Show generic error
      displayMessage(
        "❌ Server Error",
        errorMsg || "Failed to connect to the backend server. Please ensure the server is running."
      );
    }
    
    console.error("API Error:", error);
  }
}

// ==================== Initialization ====================

/**
 * Initialize application on page load
 */
function initializeApp() {
  // Load saved theme preference
  const savedTheme = localStorage.getItem("themeColor");
  if (savedTheme === "light_mode") {
    document.body.classList.add("light-theme");
    themeToggleBtn.textContent = "dark_mode";
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", initializeApp);
