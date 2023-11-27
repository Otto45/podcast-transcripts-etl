def timestamp_to_ms(timestamp: str) -> int:
    """
    Takes a timestamp string in the format HH:MM:SS and converts it to milliseconds

    Returns: An integer representing the timestamp in milliseconds
    """
    timestamp_parts = timestamp.split(':')

    if len(timestamp_parts) == 3:
        hours, minutes, seconds = map(int, timestamp_parts)
    elif len(timestamp_parts) == 2:
        hours = 0
        minutes, seconds = map(int, timestamp_parts)
    elif len(timestamp_parts) == 2:
        hours = 0
        minutes = 0
        seconds = map(int, timestamp_parts)
    else:
        raise ValueError("Invalid timestamp format")

    return (hours * 3600 + minutes * 60 + seconds) * 1000
