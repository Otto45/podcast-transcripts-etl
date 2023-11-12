import os

import assemblyai as aai
from assemblyai import Transcript

def generate_transcript(
        audio_url: str, num_speakers: int, auto_chapters = False
) -> Transcript:
    
    aai.settings.api_key = os.environ["ASSEMBLY_AI_API_TOKEN"]
    
    # We are enabling speaker diarization to label the transcript text w/ the speaker
    # NOTE: You can only enable auto_chapters or summarization individually. If we need both,
    # we'll have to submit two separate requests to the API.
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=num_speakers,
        auto_chapters=auto_chapters
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)
    
    return transcript

def get_generated_transcript(id: str) -> Transcript:
    aai.settings.api_key = os.environ["ASSEMBLY_AI_API_TOKEN"]
    
    transcript = aai.Transcript.get_by_id(id)

    return transcript
