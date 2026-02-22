from langchain_core.tools import tool
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a URL.
    
    Examples:
        https://www.youtube.com/watch?v=Ok7Q2LGvQPI  -> Ok7Q2LGvQPI
        https://youtu.be/Ok7Q2LGvQPI                  -> Ok7Q2LGvQPI
    """
    parsed_url = urlparse(url)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    return None

@tool
def get_summary(url:str)->str:
    """
    Extract the transcript from a YouTube video URL.
    Returns the transcript as a single string.
    """
    video_id=get_video_id(url)

    try:
        api_instance = YouTubeTranscriptApi()

        transcript_list = api_instance.list(video_id)

        transcript = transcript_list.find_transcript(['en'])
        
        transcript_data = transcript.fetch()

        return transcript_data

    except Exception as e:
        print(f"An error occurred: {e}")



