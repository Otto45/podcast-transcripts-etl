import feedparser
import re
from requests import get
import openai
import json

def extract_episode_timestamps_and_titles(description):
    lines = description.split('\n')
    
    # Regular expression to match (HH:MM:SS) Title format
    pattern = r'^\((\d{2}:\d{2}:\d{2})\) ([^\(]+)$'
    
    results = []
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            timestamp, title = match.groups()
            results.append({
                'timestamp': timestamp,
                'title': title.strip()
            })
    
    return results

def generate_transcript(podcast_episode):
    mp3_file = f'{podcast_episode["title"].replace(" ", "_")}.mp3'
    
    with open(mp3_file, "wb") as file:
        response = get(podcast_episode['mp3_url'])
        file.write(response.content)
    
    transcript = None

    # with open(mp3_file, "rb") as audio_file:
    #     transcript = openai.Audio.transcribe(model='whisper-1', file=audio_file, language='en')

    return transcript

feed = feedparser.parse('https://feeds.megaphone.fm/hubermanlab')

podcast_episodes = []

for entry in feed.entries[:1]:
    podcast_episodes.append({
        'original_guid': entry.id if "id" in entry else None,
        'title': entry.title,
        'link': entry.link,
        'publish_date': entry.published,
        'description': entry.description,
        'timestamps': extract_episode_timestamps_and_titles(entry.description),
        'mp3_url': entry.enclosures[0].href
    })

for podcast_episode in podcast_episodes:
    transcript = generate_transcript(podcast_episode)
    podcast_episode['transcript'] = transcript
