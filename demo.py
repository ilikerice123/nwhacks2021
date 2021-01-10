from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients
import argparse
import nltk

# target Binging with Babish video
bread_video = 'Jizr6LR83Kk'
transcript = YouTubeTranscriptApi.get_transcript(bread_video)

# Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', default=False, action='store_true')
args = parser.parse_args()

# Get verbs from db
verbs = []
with open('data/freq_words.txt', 'r') as verb_file:
    verbs = verb_file.readlines()

# Ingredient extraction
db = Ingredients()
ingreds = []
for subtitle in transcript:
	text = subtitle['text']
	stuff = db.parse_ingredients(text)
	measurements = db.parse_measurements(text)
	ingreds += stuff
	
	if (len(stuff) > 0):
		print(text)
		print(verbs)
		print(stuff)
		print(measurements)
print(ingreds)

# Filter lines
times = ['seconds', 'minutes', 'hours', 'second', 'minute', 'hour']
if args.filter:
    print("Filtering transcript...")
    for subtitle in transcript:
        text = subtitle['text']

        # Write all lines
        with open('before_filter.txt', 'a') as before_file:
            before_file.write(text + '\n')
    
        # Remove lines without an ingredient, cooking verb, or time measurement
        for ingredient, verb in zip(ingreds, verbs):
            if (ingredient in subtitle['text'] or
                    verb in subtitle['text'] or
                    len([t for t in times if(t in text)])):
                with open('after_filter.txt', 'a') as after_file:
                    after_file.write(text + '\n')
                    break


