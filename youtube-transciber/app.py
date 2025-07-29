# Import necessary tools and libraries
from youtube_transcript_api import YouTubeTranscriptApi  # Used to get the text (subtitles) from a YouTube video
from dotenv import load_dotenv  # Loads secret keys or variables from a .env file
load_dotenv()  # Load environment variables like API keys

import streamlit as st  # Streamlit is used to build the web interface
import os  # Helps in accessing environment variables like API keys
import google.generativeai as genai  # This is used to connect with Google Gemini AI model
from PIL import Image  # Used for handling images (optional here)

# Configure Gemini AI with your secret API key (stored securely in .env file)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini model (fast version)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to fetch subtitles (called transcript) from a YouTube video
def fetch_transcript(video_url):
    try:
        # Get the video ID from the YouTube link
        video_id = video_url.split("v=")[1].split("&")[0]

        # Create an object to fetch the transcript
        ytt_api = YouTubeTranscriptApi()

        # Fetch the transcript using the video ID
        fetched_transcript = ytt_api.fetch(video_id)

        # Combine all the small parts into one big string
        transcript = ""
        for snippet in fetched_transcript:
            transcript += (snippet.text + " ")  # Add each subtitle text to the transcript

        return transcript  # Return the full transcript

    except Exception as e:
        return f"An error occurred: {e}"  # If something goes wrong, show the error



prompt = """
Objective:
You are a YouTube video summarizer. Your task is to generate detailed, clear, and concise notes from the transcript of a video. You will extract the key points, steps, objectives, and other necessary details to provide an easy-to-understand summary for readers.

Instructions:

Read through the transcript and break down the video content into logical sections. Ensure that the notes cover the main points of the video.

Create Detailed Notes:

List the objectives of the video, including any goals or intended outcomes mentioned in the video.

Highlight the key steps or procedures covered in the video.

Extract and list any important concepts or definitions shared throughout the video.

If the video involves instructions, clearly outline the sequence of actions or decisions.

Identify any tools, methods, or examples mentioned in the video that aid in understanding the content.

Include any important quotes, stats, or facts that are emphasized in the video.

Break down complex sections into simplified explanations so that anyone can understand them.

Generate a Summary:

Provide a brief summary of the video that captures the essence of the entire content in a couple of sentences.

Ensure that the summary is clear, concise, and captures the core message of the video.

Language & Clarity:

The notes should be written in simple language so that anyone, regardless of their background, can understand.

Avoid jargon or use explanations for any technical terms, ensuring the content is accessible to all audiences.

Deliverables:

A list of detailed notes, organized with headings or bullet points.

A short, concise summary that captures the key takeaway of the video.

The Transcript Text will be : 

"""


# Function to get the response from Gemini AI, and stream the result chunk by chunk
def get_gemini_response(transcript_text):
    # Send the combined prompt and transcript to Gemini and ask it to stream the response
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt + "\n" + transcript_text, stream=True)

    # Go through the response in small chunks and return each part
    for chunk in response:
        yield chunk.text  # Yield means "return this piece, but keep going"

# Set up the Streamlit app title
st.title("YouTube Transcript to Detailed Notes Converter")

# Ask the user to paste a YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# If the user entered a link
if youtube_link:
    # Extract the video ID from the link
    video_arr = youtube_link.split("=")
    video_id = video_arr[1]

    # Show the video's thumbnail image
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# When the user clicks the "Get Detailed Notes" button
if st.button("Get Detailed Notes"):
    transcript = fetch_transcript(youtube_link)  # Get the transcript text from the video

    if transcript:
        st.markdown("Detailed Notes :")

        full_response = ""  # This will hold the full final result
        response_placeholder = st.empty()  # This is a blank spot on the page where we'll display text

        # Stream and show the response from Gemini as it's generated
        for chunk in get_gemini_response(transcript_text=transcript):
            full_response += chunk  # Add each small chunk to the final result
            response_placeholder.markdown(full_response)  # Show updated result on the page
