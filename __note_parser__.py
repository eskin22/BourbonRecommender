
import json
import pandas as pd
import string

from __reddit_scraper__ import RedditScraper

class NoteParser():
    def __init__(self):
        self.notes = self.get_notes_list()
        
    def get_notes_list(self):
        
        # read in the notes tracked in the notes list
        notes_list =  pd.read_csv('src/data/notes_list.csv')['notes'].to_list()
        
        # create dictionary to store counts for the notes
        notes = {}
        for note in notes_list:
            notes[note] = 0
            
        return notes
    
    def get_review_notes(self, review):
        review_no_punc = review.translate(str.maketrans('', '', string.punctuation))
        review_tokens = review_no_punc.split()
        for word in review_tokens:
            if word in self.notes.keys():
                self.notes[word] += 1
    
    

