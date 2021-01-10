from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients
import argparse
import nltk

def get_ingredients(url, filter):
    # target Binging with Babish video
    transcript = YouTubeTranscriptApi.get_transcript(url)

    # Get verbs from db
    verbs = []
    with open("../../datasets/cooking_verbs.txt", 'r') as verb_file:
        verbs = verb_file.readlines()

    # ingredient extraction
    db = Ingredients()
    ingreds = set([])
    actual_ingredients = []
    res = {}
    i = 0
    for subtitle in transcript:
        i += 1
        text = subtitle['text']
        cur_ingredients = db.parse_ingredients(text)
        measurements = db.parse_measurements(text)
        ingreds |= set(cur_ingredients)
        actual_ingredients += get_actual_ingredients(cur_ingredients, measurements)

    print(actual_ingredients)
    res['ingredients'] = actual_ingredients

    # Filter lines, creating the steps
    times = ['seconds', 'minutes', 'hours', 'second', 'minute', 'hour']
    if args.filter:
        print("Filtering transcript...")
        for subtitle in transcript:
            text = subtitle['text']

            # Write all lines
            with open('before_filter.txt', 'a') as before_file:
                before_file.write(text + '\n')
        
            # Remove lines without an ingredient, cooking verb, or time measurement
            for target in (list(ingreds) + verbs):
                if (target in text or len([t for t in times if(t in text)])):
                    with open('after_filter.txt', 'a') as after_file:
                        after_file.write(text + '\n')
                        break
    return res

def get_actual_ingredients(cur_ingredients, measurements):
    ingreds = []
    if len(cur_ingredients) > 0 and len(measurements) > 0:
        for i in range(len(cur_ingredients)):
            measurement = measurements[i] if i < len(measurements) else measurements[len(measurements) - 1]
            amount = str(measurement[0]).strip()
            unit = '' if measurement[1] is None else str(measurement[1]).strip()
            ingreds.append(amount + ' ' + unit + ' ' + str(cur_ingredients[i]).strip())
    return ingreds

def get_verbs(text):
    cur_verbs = []
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    for tag in tagged:
        if tag[1] == "VB":
            cur_verbs.append(tag[0].lower())

if __name__ == "__main__":
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', default=False, action='store_true')
    parser.add_argument('-url', '--url', required=True, type=str)

    args, unknown = parser.parse_known_args()
    get_ingredients(args.url, args.filter)
