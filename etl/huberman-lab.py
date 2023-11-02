import os
import feedparser
import json

def timestamp_to_ms(timestamp):
    hours, minutes, seconds = map(int, timestamp.split(':'))
    return (hours * 3600 + minutes * 60 + seconds) * 1000

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
                'timestamp': timestamp_to_ms(timestamp),
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

    return transcript.json_response

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

# Can be done in parallel
def process_episode(podcast_episode):
    # transcript = generate_transcript(podcast_episode['mp3_url'])
    transcript = None
    with open('transcript.json', 'r') as file:
        transcript = json.load(file)
    
    # TODO: Create document
    # TODO: Prep document for vector embedding
    # TODO: Store document and embeddings in Mongo


# Main

# feed = feedparser.parse('https://feeds.megaphone.fm/hubermanlab')

# podcast_episodes = []

# for entry in feed.entries[:1]:
#     podcast_episodes.append({
#         'original_guid': entry.id if "id" in entry else None,
#         'title': entry.title,
#         'link': entry.link,
#         'publish_date': entry.published,
#         'description': entry.description,
#         'timestamps': extract_episode_timestamps_and_titles(entry.description),
#         'mp3_url': entry.enclosures[0].href
#     })

# for podcast_episode in podcast_episodes:
#    process_episode(podcast_episode)
