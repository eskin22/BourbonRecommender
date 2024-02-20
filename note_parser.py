import pandas as pd
import requests
from bs4 import BeautifulSoup
import string
import json
from alive_progress import alive_bar
import time
import os

from __reddit_scraper__ import RedditScraper
from __rate_limiter__ import RateLimiter

notes = {
    "leather" : 0,
    "coffee" : 0,
    "tobacco" : 0,
    "licorice" : 0,
    "mint" : 0,
    "herbal tea": 0,
    "clove" : 0,
    "pepper" : 0,
    "cinnamon" : 0,
    "brown sugar" : 0,
    "chocolate" : 0,
    "baked goods" : 0,
    "butterscotch" : 0,
    "honey" : 0,
    "toffee" : 0,
    "caramel" : 0,
    "vanilla" : 0,
    "maple syrup" : 0,
    "orange" : 0,
    "lemon" : 0,
    "coconut" : 0,
    "cherry" : 0,
    "blueberry" : 0,
    "raspberry" : 0,
    "blackberry" : 0,
    "peach" : 0,
    "apple" : 0,
    "apricot" : 0,
    "prune" : 0,
    "raisin" : 0,
    "fig" : 0,
    "jam" : 0,
    "fruit" : 0,
    "rose" : 0,
    "potpurri" : 0,
    "oak" : 0,
    "pine" : 0,
    "cedar" : 0,
    "almond" : 0,
    "walnut" : 0,
    "pecan" : 0,
    "nutmeg" : 0
}

bourbon_name = "Blanton's Original Single Barrel"

print("Reading in data...")
dataset = pd.read_csv("src/data/reddit_review_archive.csv")
dataset = dataset[dataset["Whisky Name"] == bourbon_name]
reviews_list = dataset["Link To Reddit Review"].to_list()

reddit = RedditScraper()
total_review = ""

print("Extracting review data...")
total_review_count = len(reviews_list)
rate_limiter = RateLimiter(100, 60)
with alive_bar(total_review_count) as bar:
    for i, review_url in enumerate(reviews_list):
        try:
            rate_limiter.wait()
            post = reddit.get_post(review_url)
            comments = reddit.get_post_comments(post)
            review = reddit.get_review(comments)
            review = review.body
            review = review.translate(str.maketrans('', '', string.punctuation))
            total_review += review
            # print(f"Review {i+1}/{total_review_count} : Succeeded")
        except:
            # print(f"Review {i+1}/{total_review_count} : Failed")
            continue
        bar()
    
    
total_review = total_review.split()

print("Counting unigrams...")
total_review_len = len(total_review)
with alive_bar(total_review_len) as bar:
    for word in total_review:
        if word in notes.keys():
            notes[word] = notes[word] + 1
        bar()
        
with alive_bar(len(notes.keys())) as bar:
    for key, val in notes.items():
        notes[key] = val / total_review_count
        bar()
    # notes[key] = 1 if val / total_review_count >= 0.25 else 0

print("Saving results...")
dirname = bourbon_name.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower()
try:
    os.makedirs(f"data/bourbons/{dirname}")
except:
    pass
with open(f"data/bourbons/{dirname}/results.json", "w") as outfile:
    json.dump(notes, outfile, indent=4)

# notes_df = pd.DataFrame([notes])

# notes_df['bourbon_name'] = bourbon_name

# master_list = pd.read_csv("src/data/master_bourbon_list.csv")

# master_list['bourbon_name'] = master_list['bourbon_name'].str.strip()

# merged_data = pd.merge(master_list, notes_df, on="bourbon_name", how="left")

# merged_data.to_csv("src/data/master_bourbon_list.csv", index=False)
    
# print("Done.")