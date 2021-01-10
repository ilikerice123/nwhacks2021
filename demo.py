from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients

# basics with babish video on burgers: https://www.youtube.com/watch?v=iC1rvXPt_rE
video_id = 'nbCgfiqq-5c'
transcript = YouTubeTranscriptApi.get_transcript(video_id)

db = Ingredients()
ingreds = []
for subtitle in transcript:
    stuff = db.parse_ingredients(subtitle['text'])
    ingreds += stuff
print(ingreds)