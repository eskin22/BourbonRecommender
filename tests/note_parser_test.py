import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import unittest

from __note_parser__ import NoteParser

note_parser = NoteParser()

class TestNoteParser(unittest.TestCase):
    
    def test_get_review_notes(self):
        review = "this tastes like leather"
        note_parser = NoteParser()
        note_parser.get_review_notes(review)
        self.assertEqual(note_parser.notes['leather'], 1)
        
if __name__ == '__main__':
    unittest.main()