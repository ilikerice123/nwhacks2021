from youtube_transcript_api import YouTubeTranscriptApi

# binging with babish video on potstickers: https://www.youtube.com/watch?v=iC1rvXPt_rE
video_id = 'iC1rvXPt_rE'
transcript = YouTubeTranscriptApi.get_transcript(video_id)

text = ''
for subtitle in transcript:
    text += subtitle['text'] + ' '

print(text)

# def ingredients(transcript):