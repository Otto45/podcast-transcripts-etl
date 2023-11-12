from typing import List

def match_speaker_label_with_name(speaker_label: str, podcast_episode_speakers: List[str]) -> str:
    # TODO: FIX THIS METHOD TO ACTUAL PICK THE RIGHT NAME FOR THE SPEAKER LABEL
    match speaker_label:
        case 'A':
            return podcast_episode_speakers[0]
        case 'B':
            return podcast_episode_speakers[1]
        case 'C':
            return podcast_episode_speakers[2]
        case 'D':
            return podcast_episode_speakers[3]
        case 'E':
            return podcast_episode_speakers[4]
        case _:
            raise ValueError(f'Could not match speaker label "{speaker_label}" with a name')
