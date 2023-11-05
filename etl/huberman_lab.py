import os
from typing import List
import feedparser
import json

from assemblyai import Transcript

from customtypes.podcast_episode import PodcastEpisode, PodcastEpisodeTimestamp

def timestamp_to_ms(timestamp) -> int:
    hours, minutes, seconds = map(int, timestamp.split(':'))
    return (hours * 3600 + minutes * 60 + seconds) * 1000

def extract_episode_timestamps_and_titles(description) -> List[PodcastEpisodeTimestamp]:
    import re

    lines = description.split('\n')
    
    # Regular expression to match (HH:MM:SS) Title format
    pattern = r'^\((\d{2}:\d{2}:\d{2})\) ([^\(]+)$'
    
    results = []
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            timestamp, title = match.groups()
            podcast_episode_timestamp = PodcastEpisodeTimestamp(timestamp_to_ms(timestamp), title.strip())
            results.append(podcast_episode_timestamp)
    
    return results

def get_names_in_text(text: str) -> List[str]:
    import spacy

    nlp = spacy.load("en_core_web_sm")

    # Process the title to find named entities
    doc = nlp(text)

    # Extract entities labeled as 'PERSON'
    persons = set(ent.text for ent in doc.ents if ent.label_ == 'PERSON')

    # Return the unique names as a list
    return list(persons)

def generate_transcript(
        audio_url: str, num_speakers: int, auto_chapters = False
) -> Transcript:
    import assemblyai as aai

    aai.settings.api_key = os.environ["ASSEMBLY_AI_API_TOKEN"]
    
    # We are enabling speaker diarization to label the transcript text w/ the speaker
    # NOTE: You can only enable auto_chapters or summarization individually. If we need both,
    # we'll have to submit two separate requests to the API.
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=num_speakers,
        auto_chapters=auto_chapters
    )

    # transcriber = aai.Transcriber()
    # transcript = transcriber.transcribe(audio_url, config=config)
    
    transcript = aai.Transcript.get_by_id('6nzizy4gqq-6592-4a7c-9adf-00567deaef53')

    return transcript

# def prep_document_for_vector_embedding(podcast_episode, transcript):
#     from langchain.text_splitter import RecursiveCharacterTextSplitter

#     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=500, chunk_overlap=50, allowed_special="all"
#     )

#     text_chunks, metadatas = [], []

#     for utterance in transcript['utterances']:
#         utterance_metadata = {
#             'start_ms': utterance['start'],
#             'end_ms': utterance['end'],
#             'speaker': utterance['speaker']
#         }

#         utterance_chunks = text_splitter.split_text(utterance['text'])
#         metadatas_for_utterance_chunks = [utterance_metadata] * len(utterance_chunks)

#         text_chunks += utterance_chunks
#         metadatas += metadatas_for_utterance_chunks

def create_document(podcast_episode: PodcastEpisode, transcript: Transcript):
    document = {}

    document['title'] = podcast_episode.title
    document['audio_url'] = podcast_episode.audio_url
    document['description'] = podcast_episode.description
    
    if podcast_episode.original_guid is not None:
        document['original_guid'] = podcast_episode.original_guid
    
    if podcast_episode.link is not None:
        document['link'] = podcast_episode.link

    if podcast_episode.publish_date is not None:
        document['publish_date'] = podcast_episode.publish_date

    if transcript.chapters is not None:
        episode_chapters = []

        for chapter in transcript.chapters:
            episode_chapter = {
                'summary': chapter.summary,
                'gist': chapter.gist,
                'headline': chapter.headline,
                'start_ms': chapter.start,
                'end_ms': chapter.end
            }

            episode_chapters.append(episode_chapter)

        document['chapters'] = episode_chapters
    
    if podcast_episode.timestamps is not None:
        episode_timestamps = []

        for timestamp in podcast_episode.timestamps:
            episode_timestamp = {
                'title': timestamp.title,
                'timestamp_ms': timestamp.timestamp_ms
            }

            episode_timestamps.append(episode_timestamp)
        
        document['timestamps'] = episode_timestamps
    
    episode_utterances = []
    podcast_guests = get_names_in_text(podcast_episode.title)

    for utterance in transcript.utterances:
        episode_utterance = {
            'speaker': utterance.speaker, # TODO: Match speaker w/ their
            'text': utterance.text,
            'start_ms': utterance.start,
            'end_ms': utterance.end
        }

        episode_utterances.append(episode_utterance)
    
    document['transcript'] = episode_utterances
    
    return document
    
# Can be done in parallel
def process_episode(podcast_episode: PodcastEpisode):
    audio_url = podcast_episode.audio_url
    # Add one for the podcast host
    num_speakers = len(get_names_in_text(podcast_episode.title)) + 1

    transcript = generate_transcript(audio_url, num_speakers)

    document = create_document(podcast_episode, transcript)
    with open('document.json', 'w') as file:
        json.dump(document, file, indent=4)

    # TODO: Prep document for vector embedding
    # TODO: Store document and embeddings in Mongo


# Main

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
