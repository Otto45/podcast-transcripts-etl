def timestamp_to_ms(timestamp: str) -> int:
    """
    Takes a timestamp string in the format HH:MM:SS and converts it to milliseconds

    Returns: An integer representing the timestamp in milliseconds
    """
    hours, minutes, seconds = map(int, timestamp.split(':'))
    return (hours * 3600 + minutes * 60 + seconds) * 1000
