#!/usr/bin/env python3
"""Test script to verify API integration."""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

VIDEO_DATA_API_URL = os.getenv("VIDEO_DATA_API_URL", "")

if not VIDEO_DATA_API_URL:
    print("❌ VIDEO_DATA_API_URL not set in .env")
    exit(1)

print(f"🔍 Testing API endpoint: {VIDEO_DATA_API_URL}")

try:
    response = requests.get(VIDEO_DATA_API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    videos = data.get("videos", [])
    metadata = data.get("metadata", {})
    
    print(f"✅ API connection successful!")
    print(f"📊 Total videos: {len(videos)}")
    print(f"📦 Metadata: {metadata}")
    
    if videos:
        print(f"\n📹 First video:")
        first_video = videos[0]
        print(f"   ID: {first_video.get('id')}")
        print(f"   Title: {first_video.get('title')}")
        print(f"   Duration: {first_video.get('duration_formatted')}")
        print(f"   Topics: {len(first_video.get('topics', []))} topics")
        print(f"   Keywords: {len(first_video.get('keywords', []))} keywords")
        print(f"   Transcript segments: {len(first_video.get('transcript', []))}")
        print(f"   Subtitle file: {first_video.get('subtitle_file', 'N/A')}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API request failed: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n✅ All checks passed! The API integration is working correctly.")
