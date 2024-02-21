import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import unittest

from src.__classes__.__note_parser__ import NoteParser

note_parser = NoteParser()

class TestNoteParser(unittest.TestCase):
    
    def test_get_review_notes_single_review(self):
        review = "this tastes like leather and leather"
        note_parser = NoteParser()
        note_parser.get_review_notes(review)
        self.assertEqual(note_parser.notes['leather'], 1)
        
    def test_get_review_notes_multiple_reviews(self):
        review_1 = "this tastes like leather"
        review_2 = "this tastes like leather"
        note_parser.get_review_notes(review_1)
        note_parser.get_review_notes(review_2)
        self.assertEqual(note_parser.notes['leather'], 2)
        
    def test_convert_observed_notes(self):
        review_1 = "this tastes like leather"
        review_2 = "this tastes like leather"
        note_parser.get_review_notes(review_1)
        note_parser.get_review_notes(review_2)
        notes_percents = note_parser.convert_observed_notes()
        self.assertEqual(notes_percents['leather'], 1.0)
        
if __name__ == '__main__':
    unittest.main()