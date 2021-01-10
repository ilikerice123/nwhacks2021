from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients

# basics with babish video: https://www.youtube.com/watch?v=Jizr6LR83Kk
video_id = 'Jizr6LR83Kk'
transcript = YouTubeTranscriptApi.get_transcript(video_id)
import nltk

# ingredient extraction
db = Ingredients()
ingreds = []
for subtitle in transcript:
	text = subtitle['text']
	tokens = nltk.word_tokenize(text)
	tagged = nltk.pos_tag(tokens)
	verbs = []
	stuff = db.parse_ingredients(text)
	measurements = db.parse_measurements(text)
	ingreds += stuff


	for tag in tagged:
		if tag[1] == "VB":
			verbs.append(tag[0].lower())
	
	if (len(stuff) > 0):
		print(text)
		print(verbs)
		print(stuff)
		print(measurements)

print(ingreds)
