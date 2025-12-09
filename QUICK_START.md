# Quick Start Guide

## For Developers

### 🚀 Get Running in 5 Minutes

#### 1. Install Dependencies
```bash
uv sync
# or: pip install -r requirements.txt
```

#### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-key-here
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

#### 3. Run Application
```bash
uv run streamlit run app.py
```

#### 4. Open Browser
Navigate to: **http://localhost:8501**

---

## For Users

### 🎓 How to Use

1. **Click "Mulai Percakapan"** - Start voice chat with AI tutor
2. **Speak in Indonesian** - The AI understands Indonesian
3. **Ask for topics** - "Saya mau belajar hukum newton"
4. **Navigate videos** - "Pindah ke menit 2"
5. **Ask questions** - "Jelaskan isi video di detik 60"

---

## Common Commands

### Development
```bash
# Run with auto-reload
streamlit run app.py --server.runOnSave=true

# Test API connection
uv run python test_api.py

# Generate video data (if not using API)
uv run python generate_data.py
```

### Troubleshooting
```bash
# Check Python version
python --version  # Should be 3.12

# Check if API is accessible
curl http://localhost:28302/content/cards/.../raw

# Clear Streamlit cache
# In browser: Press 'C' then 'Clear cache'
```

---

## Project Structure (Simplified)

```
├── app.py                  # Main app - START HERE
├── generate_data.py        # Video processing (optional)
├── system_prompt.md        # AI tutor behavior
├── test_api.py            # Test API connection
├── data/
│   ├── videos.json        # Video metadata (cached)
│   └── subtitles/         # VTT subtitle files
├── .env                   # Your config (create this)
└── .env.example           # Config template
```

---

## Key Files to Understand

| File | Purpose | When to Edit |
|------|---------|--------------|
| `app.py` | Main application | Add features, modify UI |
| `system_prompt.md` | AI behavior | Change tutor personality/rules |
| `.env` | Configuration | Set API keys, URLs |
| `generate_data.py` | Video processing | Process new videos |

---

## Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional
- `VIDEO_DATA_API_URL` - API endpoint for video data (if not set, uses local file)

### For Video Generation Only
- `MINIO_ENDPOINT` - MinIO server
- `MINIO_ACCESS_KEY` - MinIO credentials
- `MINIO_SECRET_KEY` - MinIO credentials
- `MINIO_BUCKET` - Bucket name
- `MINIO_VIDEOS_PATH` - Path in bucket

---

## API Integration

### Using API (Recommended)
Set in `.env`:
```env
VIDEO_DATA_API_URL=http://localhost:28302/content/cards/ba7a27624af1511010900f501ddea0b7dacb3d3858ce2291efe45eb4245bdf02/raw
```

**Benefits:**
- ✅ Centralized data management
- ✅ Real-time updates
- ✅ No need to run generate_data.py

### Using Local Files
Leave `VIDEO_DATA_API_URL` empty and run:
```bash
uv run python generate_data.py
```

**Benefits:**
- ✅ Works offline
- ✅ No external dependencies

---

## Testing

### Test API Connection
```bash
uv run python test_api.py
```

**Expected output:**
```
✅ API connection successful!
📊 Total videos: 3
📹 First video: ...
✅ All checks passed!
```

### Test Voice Chat
1. Open app in browser
2. Click "Mulai Percakapan"
3. Allow microphone access
4. Say "Halo" (Hello)
5. AI should respond

### Test Video Search
1. Say "Saya mau belajar hukum newton"
2. Videos should appear
3. Click play on a video

---

## Common Issues

### Issue: "OPENAI_API_KEY tidak ditemukan"
**Solution:** Add your API key to `.env` file

### Issue: "Failed to fetch from API"
**Solution:** 
- Check if API endpoint is accessible
- Verify URL in `.env` is correct
- App will fallback to local file automatically

### Issue: No videos showing
**Solution:**
- If using API: Check API response with `test_api.py`
- If using local: Run `generate_data.py` to create videos.json

### Issue: Microphone not working
**Solution:**
- Allow microphone permission in browser
- Check browser console for errors
- Try in Chrome (best WebRTC support)

### Issue: Subtitles not showing
**Solution:**
- Check if files exist in `data/subtitles/`
- Verify file names match those in API response
- Check file permissions

---

## Next Steps

### For Developers
1. Read [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
2. Read [API_INTEGRATION.md](API_INTEGRATION.md)
3. Explore `app.py` to understand the code
4. Modify `system_prompt.md` to customize AI behavior

### For Users
1. Start the app
2. Click "Mulai Percakapan"
3. Ask the AI tutor for help
4. Explore different physics topics

---

## Resources

- **OpenAI Realtime API**: https://platform.openai.com/docs/guides/realtime
- **Streamlit Docs**: https://docs.streamlit.io/
- **WebVTT Format**: https://www.w3.org/TR/webvtt1/

---

## Support

### Documentation
- [README.md](README.md) - User guide
- [API_INTEGRATION.md](API_INTEGRATION.md) - API details
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Full technical docs

### Getting Help
1. Check documentation above
2. Run `test_api.py` to diagnose issues
3. Check browser console for errors
4. Review Streamlit logs in terminal

---

**Last Updated**: December 9, 2025  
**Version**: 1.0
