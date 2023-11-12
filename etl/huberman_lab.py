from models.podcast_episode import PodcastEpisode
from processors.podcast_episode import process_episode
from utils.podcast_episode_metadata import extract_episode_timestamps_and_titles, get_guest_names_from_title

import feedparser

feed = feedparser.parse('https://feeds.megaphone.fm/hubermanlab')

podcast_episodes = []

# for entry in feed.entries[:5]:
#     podcast_episodes.append({
#         'original_guid': entry.id if "id" in entry else None,
#         'title': entry.title,
#         'link': entry.link,
#         'publish_date': entry.published,
#         'description': entry.description,
#         'timestamps': extract_episode_timestamps_and_titles(entry.description),
#         'mp3_url': entry.enclosures[0].href
#     })

search_string = "Mark Zuckerberg & Dr. Priscilla Chan"
entry = next((entry for entry in feed.entries if search_string in entry.title), None)

podcast_episode = PodcastEpisode(
    original_guid=entry.id if "id" in entry else None,
    podcast_name="Huberman Lab",
    podcast_host="Dr. Andrew Huberman",
    guest_names=get_guest_names_from_title(entry.title),
    title=entry.title,
    link=entry.link,
    publish_date=entry.published,
    description=entry.description,
    timestamps=extract_episode_timestamps_and_titles(entry.description),
    audio_url=entry.enclosures[0].href
)

podcast_episodes.append(podcast_episode)

for podcast_episode in podcast_episodes:
   process_episode(podcast_episode)
