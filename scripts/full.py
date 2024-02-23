# add the file to the sys.path to allow execution from root directory
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# import standard packages
import pandas as pd
import string
from alive_progress import alive_bar
import plotly.graph_objects as go
import json


# import modules
from src.__classes__.__reddit_scraper__ import RedditScraper
from src.__classes__.__rate_limiter__ import RateLimiter
from src.__classes__.__note_parser__ import NoteParser
from src.__classes__.__visualizer__ import Visualizer

#TODO add the name of the bourbon you're interested in
# bourbon_name = "Blanton's Original Single Barrel"
bourbon_name = "Knob Creek 9 Small Batch"

#* Read in the links for the reddit reviews of the given bourbon
print("Reading in data...")
dataset = pd.read_csv("src/data/reddit_review_archive.csv")
dataset = dataset[dataset["Whisky Name"] == bourbon_name]
reviews_list = dataset["Link To Reddit Review"].to_list()
print("Loaded data successfully.")


with open('src/data/avg_notes_overall.json', 'r') as infile:
    notes_overall = json.load(infile)
    infile.close()

# create instance of RedditScraper object to scrape the reviews
reddit = RedditScraper()

#* Extract the reddit reviews data
print("Extracting review data...")

# create instance of RateLimiter to ensure API requests do not exceed the rate limit
rate_limiter = RateLimiter(100, 60)

# create instance of the NoteParser to extract notes from the reviews
note_parser = NoteParser()

# use alive_bar to track progress of execution
with alive_bar(len(reviews_list)) as bar:
    
    # iterate through the review URLs and try to parse them
    for i, review_url in enumerate(reviews_list):
        try:
            # use the RateLimiter.wait function to ensure safety of request
            rate_limiter.wait()
            
            # get the post information, comments on the post, and identify the review from the comments
            post = reddit.get_post(review_url)
            comments = reddit.get_post_comments(post)
            review = reddit.get_review(comments)
            review = review.body
            
            # parse the review and count the unigrams of the observed notes
            note_parser.get_review_notes(review)
        
        # if the review cannot be parsed, move on to the next 
        except:
            continue
        
        # update progress bar
        bar()

# save the results
note_parser.save_results(bourbon_name, 'info')
transformed_data = Visualizer.transform_data(note_parser.notes)
figure = Visualizer.create_notes_chart(transformed_data)
fig = figure['figure']
Visualizer.save_chart(figure, 'breakdown')

# diff = {}

# for key in note_parser.notes.keys():
#     if key == 'bourbon_name':
#         diff[key] = note_parser.notes[key]
#     else:
#         diff[key] = note_parser.notes[key] - notes_overall[key]

# note_parser.notes = diff
# note_parser.save_results(bourbon_name, 'difference_from_mean')


# transformed_data = Visualizer.transform_data(diff)
# figure = Visualizer.create_notes_chart(transformed_data)
# fig = figure['figure']
# Visualizer.save_chart(figure, 'difference_from_mean')
