from audio_transcription.functions import generate_transcript, get_generated_transcript
from models.podcast_episode import PodcastEpisode
from utils.podcast_episode_document import create_episode_document
from utils.podcast_episode_metadata import get_guest_names_from_title

# Can be done in parallel
def process_episode(podcast_episode: PodcastEpisode):
    audio_url = podcast_episode.audio_url
    num_speakers = 1

    if podcast_episode.guest_names is not None:
        num_speakers += len(podcast_episode.guest_names)

    # If the podcast does not provide timestamps for the different "chapters" of the episode, have AssemblyAI generate them
    auto_chapters = True if podcast_episode.timestamps is None or len(podcast_episode.timestamps) == 0 else False
    # transcript = generate_transcript(audio_url, num_speakers, auto_chapters)
    transcript = get_generated_transcript('6na40xqpvm-0ce9-4f3b-82af-9f039117de14')

    document = create_episode_document(podcast_episode, transcript)

    import json
    with open('episode_document.json', 'w') as file:
        json.dump(document, file, indent=4)

    # chunks, metadatas = prep_episode_document_for_vector_embedding(document)

    # create_and_save_vector_embeddings(chunks, metadatas)

    # save_episode_document(document)
