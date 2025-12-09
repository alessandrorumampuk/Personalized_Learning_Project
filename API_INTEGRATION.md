# API Integration Documentation

## Overview

This application has been enhanced to fetch video data from an external API endpoint instead of relying solely on local JSON files. This provides flexibility for centralized data management while maintaining backward compatibility with local file storage.

## Architecture

### Data Flow

```
┌─────────────────┐
│   Streamlit     │
│   Application   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  load_videos_data()             │
│  ┌───────────────────────────┐  │
│  │ 1. Try API Endpoint       │  │
│  │    (if configured)        │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│         ┌─────────┐              │
│         │ Success?│              │
│         └────┬────┘              │
│              │                   │
│      ┌───────┴────────┐          │
│      │ YES            │ NO       │
│      ▼                ▼          │
│  ┌────────┐    ┌──────────────┐ │
│  │ Return │    │ Fallback to  │ │
│  │  Data  │    │ Local File   │ │
│  └────────┘    └──────────────┘ │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Video Player   │
│  with Subtitles │
└─────────────────┘
```

## API Endpoint

### URL Format
```
http://localhost:28302/content/cards/{CARD_ID}/raw
```

### Example
```
http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

### Response Structure

The API returns a JSON object with the following structure:

```json
{
  "videos": [
    {
      "id": "video_001",
      "title": "Video Title in Indonesian",
      "description": "Detailed description of the video content",
      "filename": "downloads/original_filename.mp4",
      "url": "https://minio.pkc.pub/pkc/downloads/video.mp4",
      "duration": 787.0,
      "duration_formatted": "13:07",
      "topics": [
        "hukum newton",
        "gaya",
        "percepatan",
        "massa"
      ],
      "keywords": [
        "f=ma",
        "newton",
        "force",
        "motion"
      ],
      "transcript": [
        {
          "text": "Transcript text segment",
          "start": 0.0,
          "end": 3.0
        }
      ],
      "subtitle_file": "subtitles/video_001.vtt",
      "language": "id",
      "created_at": "2025-12-08T06:59:22.337000+00:00",
      "transcribed_at": "2025-12-09T16:38:18.135731"
    }
  ],
  "metadata": {
    "total_videos": 3,
    "last_updated": "2025-12-09T16:38:18.137041",
    "minio_bucket": "pkc",
    "minio_videos_path": "downloads",
    "minio_endpoint": "minio.pkc.pub"
  }
}
```

## Configuration

### Environment Variables

Add to your `.env` file:

```env
# Video Data API Configuration
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

### Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VIDEO_DATA_API_URL` | No | `""` | API endpoint URL. If empty, uses local file |
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for Realtime API and Whisper |

## Implementation Details

### Code Changes

#### 1. Modified `app.py`

**Added Import:**
```python
import requests
```

**Added Configuration:**
```python
VIDEO_DATA_API_URL = os.getenv("VIDEO_DATA_API_URL", "")
```

**Updated Function:**
```python
@st.cache_data
def load_videos_data() -> dict:
    """Load video data from API or fallback to local JSON file."""
    # Try to fetch from API first
    if VIDEO_DATA_API_URL:
        try:
            response = requests.get(VIDEO_DATA_API_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.warning(f"Failed to fetch from API: {e}. Falling back to local file.")
    
    # Fallback to local file
    if not VIDEOS_FILE.exists():
        return {"videos": [], "metadata": {}}
    try:
        with open(VIDEOS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"videos": [], "metadata": {}}
```

### Key Features

#### 1. **API-First Approach**
- Checks if `VIDEO_DATA_API_URL` is configured
- Makes HTTP GET request to fetch video data
- Uses 10-second timeout to prevent hanging

#### 2. **Automatic Fallback**
- If API request fails, automatically falls back to local file
- Shows warning message to user if fallback occurs
- Ensures application continues to work even if API is down

#### 3. **Caching**
- Uses Streamlit's `@st.cache_data` decorator
- Caches API responses to reduce network calls
- Cache invalidates when function parameters change or app restarts

#### 4. **Error Handling**
- Catches network errors (`requests.exceptions.RequestException`)
- Catches JSON parsing errors
- Provides graceful degradation

## Subtitle Handling

### Current Implementation

Subtitles are still loaded from **local files** in the `data/subtitles/` directory:

```python
def get_subtitle_data(subtitle_file: str | None) -> str | None:
    """Get base64 encoded subtitle data."""
    if not subtitle_file:
        return None

    subtitle_path = DATA_DIR / subtitle_file
    if subtitle_path.exists():
        with open(subtitle_path, encoding="utf-8") as f:
            vtt_content = f.read()
        encoded = base64.b64encode(vtt_content.encode()).decode()
        return f"data:text/vtt;base64,{encoded}"

    return None
```

### Why Local Subtitles?

1. **Performance**: Subtitles are embedded as base64 data URLs in the HTML
2. **Simplicity**: No additional API calls needed during video playback
3. **Reliability**: Works offline once page is loaded

### Required Files

Ensure these subtitle files exist locally:
```
data/
└── subtitles/
    ├── video_001.vtt
    ├── video_002.vtt
    └── video_003.vtt
```

## Testing

### Test API Connection

Use the provided test script:

```bash
uv run python test_api.py
```

**Expected Output:**
```
🔍 Testing API endpoint: http://localhost:28302/content/cards/.../raw
✅ API connection successful!
📊 Total videos: 3
📦 Metadata: {...}

📹 First video:
   ID: video_001
   Title: gerak harmonik sederhana pada pegas...
   Duration: 13:07
   Topics: 19 topics
   Keywords: 25 keywords
   Transcript segments: 262
   Subtitle file: subtitles/video_001.vtt

✅ All checks passed! The API integration is working correctly.
```

### Manual Testing

Test with curl:
```bash
curl -s http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw | python3 -m json.tool
```

## Deployment Scenarios

### Scenario 1: Production with API

**Setup:**
1. Configure `VIDEO_DATA_API_URL` in production `.env`
2. Ensure API endpoint is accessible from production server
3. Keep subtitle files in `data/subtitles/` directory
4. Deploy application

**Benefits:**
- Centralized video metadata management
- Easy updates without redeploying application
- Multiple applications can share same data source

### Scenario 2: Development with Local Files

**Setup:**
1. Leave `VIDEO_DATA_API_URL` empty or unset
2. Run `generate_data.py` to create local `data/videos.json`
3. Ensure subtitle files are generated

**Benefits:**
- Works offline
- No external dependencies
- Fast iteration during development

### Scenario 3: Hybrid Approach

**Setup:**
1. Configure API for production
2. Keep local files as backup
3. Application automatically falls back if API fails

**Benefits:**
- High availability
- Graceful degradation
- Best of both worlds

## Troubleshooting

### Issue: API Request Fails

**Symptoms:**
- Warning message: "Failed to fetch from API"
- Application falls back to local file

**Solutions:**
1. Check if API endpoint is accessible:
   ```bash
   curl http://localhost:28302/content/cards/.../raw
   ```
2. Verify `VIDEO_DATA_API_URL` in `.env` is correct
3. Check network connectivity
4. Verify API server is running

### Issue: No Videos Displayed

**Symptoms:**
- Empty video list in application

**Solutions:**
1. Check API response structure matches expected format
2. Verify `videos` array exists in response
3. Check browser console for JavaScript errors
4. Verify subtitle files exist locally

### Issue: Subtitles Not Showing

**Symptoms:**
- Video plays but no subtitles appear

**Solutions:**
1. Check if subtitle files exist in `data/subtitles/`
2. Verify `subtitle_file` path in API response is correct
3. Check file permissions on subtitle files
4. Verify VTT file format is valid

## API Response Requirements

### Minimum Required Fields

Each video object must have:

```json
{
  "id": "string (required)",
  "title": "string (required)",
  "url": "string (required, video URL)",
  "duration": "number (optional)",
  "duration_formatted": "string (optional)",
  "topics": "array (optional, for search)",
  "keywords": "array (optional, for search)",
  "transcript": "array (optional, for AI context)",
  "subtitle_file": "string (optional, relative path)"
}
```

### Optional Fields

- `description`: Video description
- `filename`: Original filename
- `language`: Language code (e.g., "id" for Indonesian)
- `created_at`: Creation timestamp
- `transcribed_at`: Transcription timestamp

## Performance Considerations

### Caching Strategy

- **Cache Duration**: Until app restart or manual cache clear
- **Cache Key**: Function name + parameters
- **Cache Size**: Unlimited (Streamlit default)

### Network Optimization

- **Timeout**: 10 seconds for API requests
- **Retry**: No automatic retry (fails fast)
- **Compression**: Relies on server-side gzip

### Recommendations

1. **Use CDN**: Host videos on CDN for faster loading
2. **Compress Subtitles**: VTT files are text, compress if large
3. **Lazy Loading**: Videos load on demand (already implemented)
4. **Cache Control**: Set appropriate cache headers on API

## Security Considerations

### API Endpoint

- Currently uses HTTP (localhost)
- For production, use HTTPS
- Consider API authentication if needed
- Implement rate limiting on API server

### Data Validation

- Application trusts API response structure
- Consider adding JSON schema validation
- Sanitize user inputs in search queries

### Subtitle Files

- Files are base64 encoded (safe)
- No user-uploaded content (safe)
- Served from local filesystem (safe)

## Future Enhancements

### Potential Improvements

1. **Subtitle API**: Fetch subtitles from API instead of local files
2. **Retry Logic**: Add exponential backoff for failed API requests
3. **Health Check**: Periodic API health monitoring
4. **Metrics**: Track API response times and success rates
5. **Versioning**: Support multiple API versions
6. **Webhooks**: Real-time updates when video data changes
7. **Authentication**: Add API key or OAuth support

### Example: Subtitle API Integration

```python
def get_subtitle_data(subtitle_file: str | None, video_id: str) -> str | None:
    """Get base64 encoded subtitle data from API or local file."""
    if not subtitle_file:
        return None
    
    # Try API first
    if SUBTITLE_API_URL:
        try:
            url = f"{SUBTITLE_API_URL}/{video_id}/subtitle"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            vtt_content = response.text
            encoded = base64.b64encode(vtt_content.encode()).decode()
            return f"data:text/vtt;base64,{encoded}"
        except Exception:
            pass  # Fall back to local
    
    # Fallback to local file
    subtitle_path = DATA_DIR / subtitle_file
    if subtitle_path.exists():
        with open(subtitle_path, encoding="utf-8") as f:
            vtt_content = f.read()
        encoded = base64.b64encode(vtt_content.encode()).decode()
        return f"data:text/vtt;base64,{encoded}"
    
    return None
```

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Requests Library](https://requests.readthedocs.io/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [WebVTT Specification](https://www.w3.org/TR/webvtt1/)

## Support

For issues or questions:
1. Check this documentation
2. Review `test_api.py` output
3. Check application logs
4. Verify API endpoint accessibility

---

**Last Updated**: December 9, 2025  
**Version**: 1.0  
**Author**: AI Assistant
