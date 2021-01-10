from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients

# basics with babish video on burgers: https://www.youtube.com/watch?v=iC1rvXPt_rE
video_id = 'nbCgfiqq-5c'
test = '25Od-bcv6vM&list=PLopY4n17t8RBuyIohlCY9G8sbyXrdEJls&index=2'
transcript = YouTubeTranscriptApi.get_transcript(test)
import nltk

def getVerbs():
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	for tag in tagged:
		if tag[1] == "VB":
			print(tag[0].lower())

# ingredient extraction
db = Ingredients()
ingreds = []
for subtitle in transcript:
    stuff = db.parse_ingredients(subtitle['text'])
    ingreds += stuff
# print(ingreds)

# wow
text = ''
text += subtitle['text'] + ' '
getVerbs()
