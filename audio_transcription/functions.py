import asyncio
import os

import assemblyai as aai
from assemblyai import Transcript

async def generate_transcript(
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

    # The AssemblyAI sdk uses the concurrent.futures module, so "wrap" it in an asyncio
    # executor so we can use asyncio everywhere else in our code
    loop = asyncio.get_running_loop()
    future = await loop.run_in_executor(None, transcriber.transcribe_async, audio_url, config)

    return future.result()

def get_generated_transcript(id: str) -> Transcript:
    aai.settings.api_key = os.environ["ASSEMBLY_AI_API_TOKEN"]
    
    transcript = aai.Transcript.get_by_id(id)

    return transcript
