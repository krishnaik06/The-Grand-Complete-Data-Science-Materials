import sys
from datetime import timedelta
from typing import Iterator, TextIO

from video_summarizer.exception import CustomException

def write_srt(transcript: Iterator[dict], file: TextIO):
    """
    It takes a transcript and a file object, and writes the transcript to the file in SRT format -> SubRip subTitle

    Args:
      transcript (Iterator[dict]): Iterator[dict]
      file (TextIO): The file to write the transcript to.
    """
    try:
        for i, segment in enumerate(transcript, start=1):
            print(
                f"{i}\n"
                f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
                f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
                f"{segment['text'].strip().replace('-->', '->')}\n",
                file=file,
                flush=True,
            )
    except Exception as e:
        raise CustomException(e, sys)
    
    # start: 0:02:05:45.600 -->END 0:04:05:45.600 -> 01 sec to 60 sec -> START 0:00:00:01.000  -->END 0:00:00:60.000
    # start: 0:02:05:45.600 --> END 0:04:05:45.600
    # start: 0:02:05:45.600 --> END 0:04:05:45.600


def format_timestamp(seconds: float, always_include_hours: bool = False):
    """
    It takes a float representing a number of seconds, and returns a string representing the same number
    of seconds in the format HH:MM:SS.mmm

    Args:
      seconds (float): The number of seconds to format.
      always_include_hours (bool): If True, the hours will always be included in the output. If False,
    the hours will only be included if they are non-zero. Defaults to False

    Returns:
      A string with the format:
    """
    try:
        assert seconds >= 0, "non-negative timestamp expected"
        timestamp = timedelta(seconds=seconds)
        total_seconds = int(timestamp.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d}.{timestamp.microseconds // 1000:03d}"
    except Exception as e:
        raise CustomException(e, sys)