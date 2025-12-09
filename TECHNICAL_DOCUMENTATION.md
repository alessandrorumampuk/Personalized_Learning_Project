# Technical Documentation - Physics Learning Assistant

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Data Flow](#data-flow)
7. [API Integration](#api-integration)
8. [AI Tutor System](#ai-tutor-system)
9. [Video Processing Pipeline](#video-processing-pipeline)
10. [Deployment Guide](#deployment-guide)
11. [Development Guide](#development-guide)

---

## System Overview

### Purpose

An interactive physics tutoring application for elementary school (SD) students that combines:
- Real-time voice conversation with AI tutor
- Video-based learning with synchronized subtitles
- Adaptive learning stages (7-stage pedagogy)
- Topic-based video search

### Key Features

| Feature | Description | Technology |
|---------|-------------|------------|
| **Voice Chat** | Real-time bidirectional voice conversation | OpenAI Realtime API + WebRTC |
| **Video Learning** | Physics videos with auto-generated subtitles | MinIO + HTML5 Video |
| **Topic Search** | Instant client-side video search | JavaScript keyword matching |
| **Video Navigation** | Voice-controlled timestamp navigation | Custom JavaScript API |
| **Transcript Access** | AI reads and explains video content | Whisper API transcription |
| **Adaptive Learning** | 7-stage personalized learning path | Custom prompt engineering |

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Video      │  │   WebRTC     │  │   JavaScript    │  │
│  │   Player     │  │   Audio      │  │   Search Engine │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────┬────────────────┬────────────────┬─────────────┘
             │                │                │
             │                │                │
┌────────────▼────────────────▼────────────────▼─────────────┐
│                    Streamlit Application                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  app.py - Main Application                           │  │
│  │  • Video data loading (API/Local)                    │  │
│  │  • HTML/JS generation                                │  │
│  │  • System prompt configuration                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬────────────────┬────────────────┬─────────────┘
             │                │                │
             │                │                │
┌────────────▼────────┐  ┌───▼──────────┐  ┌─▼──────────────┐
│   Video Data API    │  │   OpenAI     │  │   MinIO        │
│   (Optional)        │  │   Realtime   │  │   Storage      │
│                     │  │   API        │  │                │
│  • Video metadata   │  │              │  │  • Video files │
│  • Topics/keywords  │  │  • Voice AI  │  │  • Raw content │
│  • Transcripts      │  │  • Functions │  │                │
└─────────────────────┘  └──────────────┘  └────────────────┘
```

### Component Interaction

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ speaks
       ▼
┌─────────────────┐
│   WebRTC        │
│   (Browser)     │
└──────┬──────────┘
       │ audio stream
       ▼
┌─────────────────┐
│  OpenAI         │
│  Realtime API   │
└──────┬──────────┘
       │ response + function calls
       ▼
┌─────────────────────────────────┐
│  JavaScript Functions           │
│  • search_video()               │
│  • navigate_video()             │
│  • get_video_content()          │
└──────┬──────────────────────────┘
       │ updates UI
       ▼
┌─────────────────┐
│  Video Player   │
│  + Transcript   │
└─────────────────┘
```

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12 | Core language |
| **Streamlit** | 1.52.1 | Web framework |
| **OpenAI SDK** | 2.9.0 | AI services |
| **Requests** | 2.32.5 | HTTP client |
| **python-dotenv** | 1.2.1 | Environment config |
| **MinIO SDK** | 7.2.0+ | Object storage client |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling (modern gradient design) |
| **JavaScript (ES6+)** | Client-side logic |
| **WebRTC** | Real-time audio streaming |
| **HTML5 Video** | Video playback |

### AI Services

| Service | Model | Purpose |
|---------|-------|---------|
| **OpenAI Realtime API** | gpt-4o-realtime-preview | Voice conversation |
| **OpenAI Whisper** | whisper-1 | Video transcription |
| **OpenAI Chat** | gpt-4o-mini | Metadata extraction |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Video Storage** | MinIO (S3-compatible) | Video file hosting |
| **Data API** | Custom HTTP endpoint | Video metadata delivery |
| **Subtitles** | WebVTT format | Video captions |

---

## Project Structure

```
Personalized_Learning_MVP/
│
├── app.py                      # Main Streamlit application (1032 lines)
│   ├── load_videos_data()      # Fetch from API or local file
│   ├── load_system_prompt()    # Load AI tutor instructions
│   ├── get_subtitle_data()     # Base64 encode subtitles
│   └── get_full_app_html()     # Generate complete HTML/JS app
│
├── generate_data.py            # Video processing pipeline (523 lines)
│   ├── list_videos()           # List videos from MinIO
│   ├── download_video()        # Download to temp file
│   ├── transcribe_video()      # Whisper API transcription
│   ├── extract_metadata_with_llm()  # Generate topics/keywords
│   ├── generate_vtt()          # Create subtitle files
│   └── main()                  # Orchestrate processing
│
├── system_prompt.md            # AI tutor behavior definition
│   ├── Capabilities            # What AI can do
│   ├── Rules                   # Behavioral constraints
│   └── 7 Learning Stages       # Pedagogical framework
│
├── test_api.py                 # API integration test script
│
├── data/
│   ├── videos.json             # Video metadata (generated/cached)
│   └── subtitles/              # VTT subtitle files
│       ├── video_001.vtt
│       ├── video_002.vtt
│       └── video_003.vtt
│
├── .env                        # Environment variables (gitignored)
├── .env.example                # Environment template
├── pyproject.toml              # Python dependencies
├── requirements.txt            # Compiled dependencies
├── uv.lock                     # Dependency lock file
├── .python-version             # Python version (3.12)
├── .gitignore                  # Git ignore rules
│
├── README.md                   # User documentation
├── API_INTEGRATION.md          # API integration guide
└── TECHNICAL_DOCUMENTATION.md  # This file
```

---

## Core Components

### 1. Main Application (`app.py`)

#### Purpose
Serves the Streamlit web application with embedded HTML/JS for video player and voice chat.

#### Key Functions

##### `load_videos_data() -> dict`
```python
@st.cache_data
def load_videos_data() -> dict:
    """Load video data from API or fallback to local JSON file."""
```

**Behavior:**
1. Check if `VIDEO_DATA_API_URL` is configured
2. If yes, fetch from API with 10s timeout
3. If API fails or not configured, load from `data/videos.json`
4. Return dict with `videos` array and `metadata` object

**Caching:**
- Uses Streamlit's `@st.cache_data` decorator
- Cache persists until app restart
- Improves performance by avoiding repeated API calls

##### `get_subtitle_data(subtitle_file: str) -> str`
```python
def get_subtitle_data(subtitle_file: str | None) -> str | None:
    """Get base64 encoded subtitle data."""
```

**Behavior:**
1. Read VTT file from `data/subtitles/`
2. Encode content as base64
3. Return as data URL: `data:text/vtt;base64,{encoded}`

**Why Base64?**
- Embeds subtitles directly in HTML
- No additional HTTP requests
- Works offline once page loads

##### `get_full_app_html() -> str`
```python
def get_full_app_html(api_key: str, videos_data: list[dict], 
                      system_prompt: str) -> str:
    """Generate the complete HTML/JS application."""
```

**Generates:**
- Complete HTML document with CSS and JavaScript
- Video player with subtitle support
- WebRTC audio connection to OpenAI Realtime API
- Search functionality
- Transcript display
- Function calling handlers

**Embedded Data:**
- OpenAI API key (client-side)
- Video metadata (JSON)
- System prompt (escaped string)
- Subtitle data (base64)

### 2. Video Processing Pipeline (`generate_data.py`)

#### Purpose
Downloads videos from MinIO, transcribes them, generates rich metadata, and creates subtitle files.

#### Workflow

```
┌──────────────────┐
│  List Videos     │
│  from MinIO      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Download Video  │
│  to Temp File    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Transcribe      │
│  with Whisper    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Extract         │
│  Metadata (LLM)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Generate VTT    │
│  Subtitle File   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save to         │
│  videos.json     │
└──────────────────┘
```

#### Key Functions

##### `transcribe_video(openai_client, video_path) -> dict`
```python
def transcribe_video(openai_client: OpenAI, video_path: str) -> dict | None:
    """Transcribe video using OpenAI Whisper API."""
```

**Parameters:**
- `language="id"` (Indonesian)
- `response_format="verbose_json"`
- `timestamp_granularities=["segment"]`

**Returns:**
```python
{
    "segments": [{"text": str, "start": float, "end": float}],
    "full_text": str,
    "duration": float,
    "language": "id"
}
```

##### `extract_metadata_with_llm() -> dict`
```python
def extract_metadata_with_llm(openai_client: OpenAI, 
                              filename: str, 
                              transcript_text: str) -> dict:
    """Use LLM to extract title, description, and rich topics."""
```

**LLM Prompt Strategy:**
- Analyzes filename and transcript
- Generates 30-50 topics/keywords total
- Topics (15-25): Main concepts, sub-topics, related concepts
- Keywords (15-25): Terminology, synonyms (ID/EN), common queries
- All lowercase for better matching

**Example Output:**
```python
{
    "title": "Gerak Harmonik Sederhana pada Pegas",
    "description": "Video mengulas gerak harmonik...",
    "topics": ["hukum newton", "gaya pegas", "energi"],
    "keywords": ["f=ma", "hooke's law", "spring constant"]
}
```

##### `generate_vtt(segments) -> str`
```python
def generate_vtt(segments: list[dict]) -> str:
    """Generate WebVTT subtitle content from segments."""
```

**Output Format:**
```
WEBVTT

1
00:00:00.000 --> 00:00:03.000
Dalam video ini, kita akan melihat simpel motion harmonik.

2
00:00:03.000 --> 00:00:06.000
Kita akan mulai dengan jaring vertikal.
```

### 3. AI Tutor System (`system_prompt.md`)

#### 7-Stage Learning Framework

| Stage | Name | Purpose | AI Actions |
|-------|------|---------|------------|
| **1** | Belajar Sambil Bermain | Assess baseline | Give progressive difficulty questions |
| **2** | Evaluasi dan Saran Adaptif | Personalize path | Recommend videos based on performance |
| **3** | Pemahaman Konsep | Check understanding | Ask explanation questions |
| **4** | Pujian dan Reward | Motivate | Give praise and certificate tokens |
| **5** | Latihan Terarah | Target weaknesses | Practice weak areas |
| **6** | Mastery Learning | Achieve perfection | Practice until perfect score |
| **7** | Tantangan & Kompetisi | Engage long-term | Challenges and leaderboards |

#### Function Calling

The AI tutor has access to three JavaScript functions:

##### `search_video(query: string)`
```javascript
// Searches videos by topics/keywords
// Returns: Array of matching videos sorted by relevance
```

**When to call:**
- User asks to learn a topic: "Saya mau belajar hukum newton"
- User searches for content: "Ada video tentang gaya?"

##### `get_video_content(timestamp: number)`
```javascript
// Gets transcript text at specific timestamp
// Returns: String with transcript content
```

**When to call:**
- User asks about video content: "Isi detik 60 tentang apa?"
- AI needs context: "Di menit 2 membahas apa?"

##### `navigate_video(timestamp: number)`
```javascript
// Seeks video to specific timestamp
// Returns: Confirmation message
```

**When to call:**
- User requests navigation: "Pindah ke detik 30"
- AI suggests reviewing: "Mari kita lihat bagian di menit 1"

---

## Data Flow

### Video Data Loading

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Start                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ VIDEO_DATA_API_URL   │
              │ configured?          │
              └──────────┬───────────┘
                         │
           ┌─────────────┴─────────────┐
           │ YES                       │ NO
           ▼                           ▼
┌────────────────────┐      ┌──────────────────┐
│  Fetch from API    │      │  Load Local File │
│  (10s timeout)     │      │  videos.json     │
└─────────┬──────────┘      └────────┬─────────┘
          │                          │
          │ Success?                 │
          ├──────────┐               │
          │ YES      │ NO            │
          ▼          ▼               │
     ┌────────┐  ┌────────┐         │
     │ Return │  │ Warn & │         │
     │  Data  │  │Fallback│         │
     └────────┘  └───┬────┘         │
                     │               │
                     └───────┬───────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │  Cache Data      │
                  │  (@st.cache_data)│
                  └──────────┬───────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │  Generate HTML   │
                  │  with Video Data │
                  └──────────────────┘
```

### Voice Conversation Flow

```
┌─────────────┐
│   User      │
│   Speaks    │
└──────┬──────┘
       │ audio
       ▼
┌──────────────────────┐
│  Browser WebRTC      │
│  • Capture mic       │
│  • Send to OpenAI    │
└──────┬───────────────┘
       │ WebSocket
       ▼
┌──────────────────────┐
│  OpenAI Realtime API │
│  • Process audio     │
│  • Generate response │
│  • Call functions    │
└──────┬───────────────┘
       │
       ├─────────────────┬─────────────────┐
       │ audio response  │ function call   │ text response
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Play Audio  │  │  Execute JS  │  │  Show Text   │
│  in Browser  │  │  Function    │  │  in Chat     │
└──────────────┘  └──────┬───────┘  └──────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Update UI           │
              │  • Search results    │
              │  • Video navigation  │
              │  • Transcript view   │
              └──────────────────────┘
```

---

## API Integration

### Configuration

**Environment Variable:**
```env
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

### API Contract

**Request:**
```http
GET /content/cards/{CARD_ID}/raw HTTP/1.1
Host: localhost:28302
```

**Response:**
```json
{
  "videos": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "url": "string",
      "duration": "number",
      "duration_formatted": "string",
      "topics": ["string"],
      "keywords": ["string"],
      "transcript": [
        {"text": "string", "start": "number", "end": "number"}
      ],
      "subtitle_file": "string"
    }
  ],
  "metadata": {
    "total_videos": "number",
    "last_updated": "string",
    "minio_bucket": "string"
  }
}
```

### Error Handling

**Network Errors:**
- Timeout after 10 seconds
- Show warning to user
- Fallback to local file

**JSON Errors:**
- Catch parsing exceptions
- Fallback to local file

**Missing Data:**
- Return empty structure: `{"videos": [], "metadata": {}}`

### Testing

**Test Script:**
```bash
uv run python test_api.py
```

**Manual Test:**
```bash
curl -s http://localhost:28302/content/cards/.../raw | jq .
```

---

## Deployment Guide

### Prerequisites

- Python 3.12
- OpenAI API key
- MinIO credentials (for video generation)
- API endpoint (for video data)

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Personalized_Learning_MVP
   ```

2. **Install Dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Setup Video Data**
   
   **Option A: Use API**
   ```env
   VIDEO_DATA_API_URL=http://your-api-endpoint/raw
   ```
   
   **Option B: Generate Locally**
   ```bash
   uv run python generate_data.py
   ```

5. **Run Application**
   ```bash
   uv run streamlit run app.py
   ```

6. **Access Application**
   ```
   http://localhost:8501
   ```

### Production Deployment

#### Using Docker (Recommended)

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
docker build -t physics-tutor .
docker run -p 8501:8501 --env-file .env physics-tutor
```

#### Using Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard:
   - `OPENAI_API_KEY`
   - `VIDEO_DATA_API_URL`
4. Deploy

#### Environment Variables for Production

```env
# Required
OPENAI_API_KEY=sk-...
VIDEO_DATA_API_URL=https://api.example.com/videos

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

---

## Development Guide

### Local Development Setup

1. **Create Virtual Environment**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install black flake8 mypy  # Optional: code quality tools
   ```

3. **Run in Development Mode**
   ```bash
   streamlit run app.py --server.runOnSave=true
   ```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Document functions with docstrings

**JavaScript:**
- Use ES6+ features
- Prefer `const` over `let`
- Use async/await for promises

### Testing

**Test API Integration:**
```bash
uv run python test_api.py
```

**Test Video Processing:**
```bash
uv run python generate_data.py
# Enter 1 when prompted (process 1 video for testing)
```

**Manual Testing Checklist:**
- [ ] Voice chat connects successfully
- [ ] Video plays with subtitles
- [ ] Search returns relevant results
- [ ] Video navigation works via voice
- [ ] Transcript displays correctly
- [ ] AI responds appropriately

### Debugging

**Enable Streamlit Debug Mode:**
```bash
streamlit run app.py --logger.level=debug
```

**Check Browser Console:**
- Open DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| No audio | Mic permissions | Allow mic access in browser |
| API timeout | Slow network | Increase timeout in code |
| No videos | Missing data | Check API or run generate_data.py |
| Subtitles missing | File not found | Verify files in data/subtitles/ |

### Adding New Features

**Example: Add New Function for AI**

1. **Define in system_prompt.md:**
   ```markdown
   - Gunakan get_quiz_question() untuk memberikan soal latihan
   ```

2. **Implement in JavaScript (app.py):**
   ```javascript
   {
       name: "get_quiz_question",
       description: "Get a random quiz question",
       parameters: {
           type: "object",
           properties: {
               difficulty: {
                   type: "string",
                   enum: ["easy", "medium", "hard"]
               }
           }
       }
   }
   ```

3. **Add Handler:**
   ```javascript
   async function handleFunctionCall(functionCall) {
       if (functionCall.name === "get_quiz_question") {
           const difficulty = functionCall.arguments.difficulty;
           const question = getRandomQuiz(difficulty);
           return JSON.stringify(question);
       }
   }
   ```

---

## Appendix

### Glossary

- **WebRTC**: Web Real-Time Communication protocol for audio/video streaming
- **VTT**: WebVTT (Web Video Text Tracks) subtitle format
- **MinIO**: S3-compatible object storage system
- **Realtime API**: OpenAI's API for real-time voice conversations
- **Whisper**: OpenAI's speech-to-text model

### File Formats

**videos.json Structure:**
```json
{
  "videos": [...],
  "metadata": {
    "total_videos": 3,
    "last_updated": "2025-12-09T16:38:18.137041",
    "minio_bucket": "pkc",
    "minio_videos_path": "downloads",
    "minio_endpoint": "minio.pkc.pub"
  }
}
```

**VTT Format:**
```
WEBVTT

1
00:00:00.000 --> 00:00:03.000
Text content here

2
00:00:03.000 --> 00:00:06.000
More text content
```

### Performance Metrics

**Typical Response Times:**
- API fetch: 100-500ms
- Video load: 1-3s (depends on size)
- Voice latency: 200-500ms
- Search: <50ms (client-side)

### Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |

**Required Features:**
- WebRTC
- HTML5 Video
- ES6 JavaScript
- WebSocket

---

**Document Version**: 1.0  
**Last Updated**: December 9, 2025  
**Maintained By**: Development Team
