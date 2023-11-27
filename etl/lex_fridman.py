import asyncio
import os
import requests
from typing import List
from databases.document import get_episode_titles
from models.podcast_episode import PodcastEpisode
from processors.podcast_episode import process_new_episode
from utils.podcast_episode_metadata import extract_episode_timestamps_and_titles, get_guest_names_from_title

import feedparser

async def main():
    PODCAST_NAME = 'Lex Fridman Podcast'
    RSS_FILE_NAME = 'lex_fridman_rss'

    rss_file_response = requests.get('https://lexfridman.com/feed/podcast/')

    if rss_file_response.status_code == 200:
        with open(RSS_FILE_NAME, 'wb') as file:
            file.write(rss_file_response.content)
    else:
        print(f'Failed to download the {PODCAST_NAME} RSS feed')
    
    feed = feedparser.parse(RSS_FILE_NAME)
    # Sort by published date desc
    sorted_entries = sorted(feed.entries, key=lambda e: e.published_parsed, reverse=True)

    prev_processed_episode_titles = get_episode_titles(PODCAST_NAME)

    podcast_episodes: List[PodcastEpisode] = []

    for entry in sorted_entries[:5]:
        if entry.title in prev_processed_episode_titles:
            continue

        print(f'Processing {PODCAST_NAME} episode: {entry.title}')
        
        podcast_episodes.append(PodcastEpisode(
        original_guid=entry.id if 'id' in entry else None,
        podcast_name=PODCAST_NAME,
        podcast_host='Lex Fridman',
        guest_names=get_guest_names_from_title(entry.title),
        title=entry.title,
        link=entry.link,
        publish_date=entry.published,
        description=entry.description,
        timestamps=extract_episode_timestamps_and_titles(entry.description),
        audio_url=entry.enclosures[0].href))

    tasks = [process_new_episode(podcast_episode) for podcast_episode in podcast_episodes]
    await asyncio.gather(*tasks)

    os.remove(RSS_FILE_NAME)
    
asyncio.run(main())
