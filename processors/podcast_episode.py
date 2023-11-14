from audio_transcription.functions import generate_transcript, get_generated_transcript
from databases.document import save_episode_document
from databases.vector import create_and_save_vector_embeddings
from models.podcast_episode import PodcastEpisode
from utils.podcast_episode_document import create_episode_document

async def process_new_episode(podcast_episode: PodcastEpisode):
    audio_url = podcast_episode.audio_url
    num_speakers = 1

    if podcast_episode.guest_names is not None:
        num_speakers += len(podcast_episode.guest_names)

    # If the podcast does not provide timestamps for the different "chapters" of the episode, have AssemblyAI generate them
    auto_chapters = True if podcast_episode.timestamps is None or len(podcast_episode.timestamps) == 0 else False
    transcript = await generate_transcript(audio_url, num_speakers, auto_chapters)

    document = create_episode_document(podcast_episode, transcript)

    save_episode_document(document)
    
    # Embeddings will get created when speakers are matched with their names,
    # if there are more than one guest on the episode
    if 'speaker-names' not in document:
        create_and_save_vector_embeddings(document)
