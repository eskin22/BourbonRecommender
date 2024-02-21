
import json
import pandas as pd
import string
import os

class NoteParser():
    def __init__(self):
        self.notes = self.get_notes_list()
        self.total_reviews = 0
        
    def get_notes_list(self):
        
        # read in the notes tracked in the notes list
        notes_list =  pd.read_csv('src/data/notes_list.csv')['notes'].to_list()
        
        # create dictionary to store counts for the notes
        notes = {'bourbon_name': None}
        for note in notes_list:
            notes[note] = 0
            
        return notes
    
    def get_review_notes(self, review):
        
        # remove the punctuation and split the review to extract unigrams
        review_no_punc = review.translate(str.maketrans('', '', string.punctuation))
        review_tokens = review_no_punc.split()
        
        # create notes set to ensure we don't overcount notes for a review
        notes_observed = set()
        
        # iterate through the words in the review and increment the count for observed notes
        for word in review_tokens:
            if word in self.notes.keys():
                if word not in notes_observed:
                    notes_observed.add(word)
                    self.notes[word] += 1
                    
        # increment total reviews
        self.total_reviews += 1
                    
    def save_results(self, bourbon_name, fnc):
        
        self.notes['bourbon_name'] = bourbon_name
        
        # convert the notes to percentages of observance across all reviews
        self.convert_observed_notes()
        
        # format bourbon name for FNC by removing punctuation and replacing spaces
        dirname = bourbon_name.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower()
        
        # create a new directory for the bourbon if one does not already exist
        try:
            os.makedirs(f"data/bourbons/{dirname}")
        except:
            pass
        
        # save the observed notes into a .json file
        with open(f"data/bourbons/{dirname}/{fnc}.json", "w") as outfile:
            json.dump(self.notes, outfile, indent=4)
            
    def convert_observed_notes(self):
        
        # create dict to store note percentages across all reviews
        notes_percents = {}
        
        # iterate through the notes and compute percentage of note observance across all reviews
        for key, val in self.notes.items():
            if key == 'bourbon_name':
                notes_percents[key] = val
            else:
                notes_percents[key] = val / self.total_reviews
        
        self.notes = notes_percents
    
    

