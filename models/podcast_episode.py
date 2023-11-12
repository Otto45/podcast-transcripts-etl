from typing import List

class PodcastEpisodeTimestamp:
    
    def __init__(self, timestamp_ms: int, title: str):
        self.timestamp_ms = timestamp_ms
        self.title = title

class PodcastEpisode:

    def __init__(
            self,
            podcast_name: str,
            podcast_host: str,
            title: str,
            audio_url: str,
            description: str,
            guest_names: List[str] = None,
            original_guid: str = None,
            link: str = None,
            publish_date: str = None,
            timestamps: List[PodcastEpisodeTimestamp] = None
    ):

        self.podcast_name = podcast_name
        self.podcast_host = podcast_host
        self.title = title
        self.audio_url = audio_url
        self.description = description
        self.guest_names = guest_names
        self.original_guid = original_guid
        self.link = link
        self.publish_date = publish_date
        self.timestamps = timestamps
