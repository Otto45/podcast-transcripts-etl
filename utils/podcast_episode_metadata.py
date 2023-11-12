import json
from typing import List
import re

from models.podcast_episode import PodcastEpisodeTimestamp
from utils.timestamp import timestamp_to_ms

from openai import OpenAI

def extract_episode_timestamps_and_titles(description: str) -> List[PodcastEpisodeTimestamp]:
    lines = description.split('\n')
    
    # Regular expression to match (HH:MM:SS) Title format
    pattern = r'^\((\d{2}:\d{2}:\d{2})\)\s(.+)$'
    
    results = []
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            timestamp, title = match.groups()
            podcast_episode_timestamp = PodcastEpisodeTimestamp(timestamp_to_ms(timestamp), title.strip())
            results.append(podcast_episode_timestamp)
    
    return results

def get_guest_names_from_title(title: str, openai_model = 'gpt-4-1106-preview') -> List[str]:
    client = OpenAI()

    prompt = f"""
Hello! Please return a JSON list containing people's names from the following text:

"{title}"

Also, if the person has a title, like "Mr", "Mrs", "Ms", "Dr", etc., please include it with their name.
Here is an example:

Text: "Steve Austin & Dr. Chow: The Ultimate Mashup!"

JSON: {{ "names": ["Steve Austin", "Dr. Chow"]}}

If there are no people's names in the text, please respond with an empty JSON object, like this:

{{}}

When you respond, ONLY RESPOND WITH A JSON STRING, NOT WITH MARKDOWN OR ANY OTHER FORMATTING!!!
"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model=openai_model
    )

    names = None

    print(chat_completion)

    if len(chat_completion.choices) > 0 and chat_completion.choices[0].message.content is not None:
        json_response = json.loads(chat_completion.choices[0].message.content)

        if 'names' in json_response:
            names = json_response['names']

    return names
