import asyncio
from typing import List
from models.podcast_episode import PodcastEpisode
from processors.podcast_episode import process_new_episode
from utils.podcast_episode_metadata import extract_episode_timestamps_and_titles, get_guest_names_from_title

import feedparser

async def main():
    feed = feedparser.parse('https://feeds.megaphone.fm/hubermanlab')
    # Sort by published date desc
    sorted_entries = sorted(feed.entries, key=lambda e: e.published_parsed, reverse=True)

    podcast_episodes: List[PodcastEpisode] = []

    for entry in sorted_entries[:10]:
        podcast_episodes.append(PodcastEpisode(
        original_guid=entry.id if "id" in entry else None,
        podcast_name="Huberman Lab",
        podcast_host="Dr. Andrew Huberman",
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
