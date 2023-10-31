import os
import feedparser
import json

def extract_episode_timestamps_and_titles(description):
    import re

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

def generate_transcript(mp3_url):
    import assemblyai as aai

    aai.settings.api_key = os.environ["ASSEMBLY_AI_API_TOKEN"]
    
    # We are enabling speaker diarization to label the transcript text w/ the speaker
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(mp3_url, config=config)
    
    with open('transcript.json', 'w') as file:
        json.dump(transcript.json_response, file, indent=4)
    
    with open('chapters.json', 'w') as file:
        json.dump(transcript.chapters, file, indent=4)

    with open('transcript.txt', 'w') as file:
        file.write(transcript.text)

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
    transcript = generate_transcript(podcast_episode['mp3_url'])
    # podcast_episode['transcript'] = transcript
