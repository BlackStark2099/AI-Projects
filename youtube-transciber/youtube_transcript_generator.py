from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1].split("&")[0]
        # Extract video ID from the URL
        ytt_api = YouTubeTranscriptApi()

        # Fetch the transcript
        fetched_transcript = ytt_api.fetch(video_id)
        transcript = ""
        for snippet in fetched_transcript:
            transcript += (snippet.text + " ")
        

        print(transcript)

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
youtube_link = "https://www.youtube.com/watch?v=k2P_pHQDlp0" # Replace with an actual YouTube video URL
transcript = get_youtube_transcript(youtube_link)
print(transcript)