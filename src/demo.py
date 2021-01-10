from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients
import argparse
import nltk

def get_ingredients(url):
    # target Binging with Babish video
    bread_video = 'Jizr6LR83Kk'
    transcript = YouTubeTranscriptApi.get_transcript(str(url))

    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', default=False, action='store_true')
    args, unknown = parser.parse_known_args()

    # Get verbs from db
    verbs = []
    old_string = "../datasets/cooking_verbs.txt" 
    curr = "../../datasets/cooking_verbs.txt"
    with open(curr, 'r') as verb_file:
        verbs = verb_file.readlines()

    # ingredient extraction
    db = Ingredients()
    ingreds = []
    res = {}
    i = 0
    for subtitle in transcript:
        res[i] = subtitle['text']
        i += 1
        text = subtitle['text']
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        verbs1 = []
        stuff = db.parse_ingredients(text)
        measurements = db.parse_measurements(text)
        ingreds += stuff

        for tag in tagged:
            if tag[1] == "VB":
                verbs1.append(tag[0].lower())
        
        if (len(stuff) > 0):
            print(text)
            print(verbs1)
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
    print(res)
    return res

if __name__ == "__main__":
    get_ingredients("Jizr6LR83Kk")
