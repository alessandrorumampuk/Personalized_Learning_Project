# Physics Learning Assistant

Aplikasi tutor fisika interaktif menggunakan OpenAI Realtime API untuk percakapan suara real-time dengan video pembelajaran.

## Features

- **Voice Chat** - Percakapan suara real-time dengan AI tutor menggunakan OpenAI Realtime API + WebRTC
- **Video Learning** - Video pembelajaran fisika dengan subtitle otomatis
- **Topic Search** - Pencarian video berdasarkan topik/kata kunci (instant, tanpa API call)
- **Video Navigation** - Navigasi ke timestamp tertentu via voice command
- **Transcript Access** - AI dapat membaca dan menjelaskan isi video di setiap detik

## Tech Stack

- **Frontend**: Streamlit + HTML/JavaScript (WebRTC)
- **AI Voice**: OpenAI Realtime API (gpt-4o-realtime-preview)
- **Transcription**: OpenAI Whisper API
- **Video Storage**: MinIO (S3-compatible)
- **Search**: Topic-based keyword matching (client-side)

## Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` ke `.env` dan isi kredensial:

```bash
cp .env.example .env
```

```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# MinIO Configuration (for generate_data.py)
MINIO_ENDPOINT=play.min.io
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET=physics-videos
MINIO_VIDEOS_PATH=downloads
MINIO_SECURE=true

# Max videos to process (0 = no limit)
MAX_VIDEOS=0

# Video Data API (optional - if not set, uses local data/videos.json)
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

### 3. Video Data Setup

**Option A: Use API Endpoint (Recommended)**

Set `VIDEO_DATA_API_URL` in `.env` to fetch video data from an API:
```env
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

The app will automatically fetch video metadata from this endpoint. Make sure subtitle files exist in `data/subtitles/` directory.

**Option B: Generate Local Video Data**

If not using API, generate local data by running:

```bash
uv run python generate_data.py
```

This script will:
- Download video dari MinIO
- Transcribe menggunakan Whisper API
- Generate rich topics/keywords menggunakan LLM
- Simpan metadata ke `data/videos.json`

Akan muncul prompt untuk memasukkan jumlah maksimal video yang ingin diproses.

### 4. Run Application

```bash
uv run streamlit run app.py
```

Buka http://localhost:8501 di browser.

## Usage

1. Klik **"Mulai Percakapan"** untuk memulai voice chat
2. Bicara dengan AI tutor dalam Bahasa Indonesia
3. Contoh perintah:
   - "Saya mau belajar hukum newton"
   - "Jelaskan isi video di detik 60"
   - "Pindah ke menit 2"

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── generate_data.py    # Video transcription & metadata generator
├── data/
│   ├── videos.json     # Video metadata with topics/keywords
│   └── subtitles/      # VTT subtitle files
├── .env.example        # Environment variables template
├── pyproject.toml      # Python dependencies
└── README.md
```

## How Search Works

Pencarian menggunakan **topic-based matching** yang berjalan di browser:

1. Setiap video memiliki 30-50 topics/keywords yang di-generate oleh LLM
2. Query user di-match dengan topics, keywords, dan title
3. Video di-score berdasarkan jumlah keyword match
4. Hasil instant tanpa API call (WebRTC tetap connected)

## Documentation

For detailed technical information, see:

- **[API_INTEGRATION.md](API_INTEGRATION.md)** - Complete guide to API integration, configuration, and troubleshooting
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Comprehensive technical documentation covering architecture, components, and development

## License

MIT
