from youtube_transcript_api import YouTubeTranscriptApi
from ingredients import Ingredients
import argparse
import nltk
import pytube
import numpy as np
import cv2
import os

PICTURE_FREQUENCY = 8

def get_recipe(url, use_filter):
    # target Binging with Babish video
    transcript = YouTubeTranscriptApi.get_transcript(url)

    # Get verbs from db
    verbs = []
    with open("../../datasets/cooking_verbs.txt", 'r') as verb_file:
        verbs = verb_file.readlines()

    # ingredient extraction ============================
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
    # ==================================================
    video_file = download_video(url)

    # steps extraction =================================
    times = ['seconds', 'minutes', 'hours', 'second', 'minute', 'hour']
    instructions = []
    pictures = []
    if use_filter:
        i = 0
        for subtitle in transcript:
            text = subtitle['text']

            # Write all lines
            # with open('before_filter.txt', 'a') as before_file:
            #     before_file.write(text + '\n')
        
            # Remove lines without an ingredient, cooking verb, or time measurement
            for target in (list(ingreds) + verbs):
                if (target in text or len([t for t in times if(t in text)])):
                    instructions.append({'step': text})
                    if i % PICTURE_FREQUENCY == 0:
                        pictures.append(subtitle['start'])
                    # with open('after_filter.txt', 'a') as after_file:
                    #     after_file.write(text + '\n')
                    #     break
                    i += 1
                    break
    res['instructions'] = instructions
    # ==================================================

    # frames extraction ================================
    file_names = extract_frames(video_file, pictures)
    i = 0
    for file_name in file_names:
        res['instructions'][i]['image'] = file_name
        i += PICTURE_FREQUENCY
    if os.path.exists(video_file):
        os.remove(video_file)
    # ==================================================

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

def download_video(video_id):
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    youtube = pytube.YouTube(video_url)
    video = youtube.streams.first()
    video.download('frames', video_id + '.mp4') # path, where to video download.
    return 'frames/' + video_id + 'mp4.mp4'

def extract_frames(video_file, frame_secs):
    #Open the video file
    cap = cv2.VideoCapture(video_file)
    name_prefix = video_file.split(".")[0]
    files = []

    #The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
    #Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
    #The second argument defines the frame number in range 0.0-1.0
    for frame_sec in frame_secs:
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_sec * 1000)
        ret, frame = cap.read()
        file_name = name_prefix + '_frame' + str(frame_sec) + '.jpg'
        #Store this frame to an image
        cv2.imwrite(file_name, frame)
        files.append(file_name)

    # When everything done, release the capture
    cap.release()
    return files

if __name__ == "__main__":
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', default=False, action='store_true')
    parser.add_argument('-url', '--url', required=True, type=str)

    args, unknown = parser.parse_known_args()
    a = get_recipe(args.url, args.filter)
    print(len(a['instructions']))
    print(a)
