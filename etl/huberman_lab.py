import asyncio
from typing import List
from databases.document import get_episode_titles
from models.podcast_episode import PodcastEpisode
from processors.podcast_episode import process_new_episode
from utils.podcast_episode_metadata import extract_episode_timestamps_and_titles, get_guest_names_from_title

import feedparser

async def main():
    PODCAST_NAME = 'Huberman Lab'
    
    feed = feedparser.parse('https://feeds.megaphone.fm/hubermanlab')
    # Sort by published date desc
    sorted_entries = sorted(feed.entries, key=lambda e: e.published_parsed, reverse=True)

    prev_processed_episode_titles = get_episode_titles(PODCAST_NAME)

    podcast_episodes: List[PodcastEpisode] = []

    for entry in sorted_entries[:5]:
        if entry.title in prev_processed_episode_titles:
            continue
        
        podcast_episodes.append(PodcastEpisode(
        original_guid=entry.id if 'id' in entry else None,
        podcast_name=PODCAST_NAME,
        podcast_host='Dr. Andrew Huberman',
        guest_names=get_guest_names_from_title(entry.title),
        title=entry.title,
        link=entry.link,
        publish_date=entry.published,
        description=entry.description,
        timestamps=extract_episode_timestamps_and_titles(entry.description),
        audio_url=entry.enclosures[0].href))

    tasks = [process_new_episode(podcast_episode) for podcast_episode in podcast_episodes]
    await asyncio.gather(*tasks)
        

asyncio.run(main())
