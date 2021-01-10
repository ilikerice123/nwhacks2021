from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from collections import OrderedDict

verb_db = {}
NUM_VIDEOS_PLAYLIST = 96

# Read from videos.txt
videos = open("videos.txt", "r")
lines = videos.readlines()

for line in lines:
    print(line)
    # Basics with Babish video on burgers: https://www.youtube.com/watch?v=iC1rvXPt_rE
    playlist_url = line
    transcript = YouTubeTranscriptApi.get_transcript(playlist_url)
    # Separate into sections
    for subtitle in transcript:
        text = subtitle['text']
        # Parse sentence into tokens
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)

        # Count verbs
        for tag in tagged:
            if tag[1] == "VB":
                if tag[0].lower() not in verb_db:
                    verb_db[tag[0].lower()] = 1
                else:
                    verb_db[tag[0].lower()] += 1

verb_db_s = sorted(verb_db.items(), key=lambda x: x[1], reverse=True)
print(verb_db_s)

# Clear text file
open("cooking_verbs.txt", "w").close()

# Write verbs into text file
with open("cooking_verbs.txt", "a") as output_file:
    for word in verb_db_s:
        output_file.write(str(word[0]) + "\n")
