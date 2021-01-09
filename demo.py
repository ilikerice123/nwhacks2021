from youtube_transcript_api import YouTubeTranscriptApi
import nltk

# binging with babish video on potstickers: https://www.youtube.com/watch?v=iC1rvXPt_rE
video_id = 'iC1rvXPt_rE'
lotr_special = 'g09731mD-s8'
transcript = YouTubeTranscriptApi.get_transcript(lotr_special)

def getVerbs():
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	for tag in tagged:
		if tag[1] == "VB":
			print(tag[0].lower())

text = ''
for subtitle in transcript:
    text += subtitle['text'] + ' '
getVerbs()

