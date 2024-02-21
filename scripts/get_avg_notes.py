import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
import json
import string

from src.__classes__.__visualizer__ import Visualizer

# notes_list =  pd.read_csv('src/data/notes_list.csv')['notes'].to_list()

# notes_overall = {}

# for note in notes_list:
#     notes_overall[note] = []
    
# for file in os.listdir('data/bourbons'):
#     with open(f'data/bourbons/{file}/info.json', 'r') as infile:
#         data = json.load(infile)
#         infile.close()
#     for key, val in data.items():
#         if key in notes_overall:
#             notes_overall[key].append(val)

# for key in notes_overall.keys():
#     notes_overall[key] = sum(notes_overall[key]) / len(notes_overall[key])


# read in the average note percentages overall
with open('get_avg_notes_results.json', 'r') as infile:
    notes_overall = json.load(infile)
    infile.close()
    
for file in os.listdir('data/bourbons'):
    
    # read in the data for a given bourbon
    with open(f'data/bourbons/{file}/info.json', 'r') as infile:
        data = json.load(infile)
        infile.close()
    
    # create dict to store differences observed
    diff = {}
    
    # find the difference from the average for each note
    for key in data.keys():
        if key == 'bourbon_name':
            diff[key] = data[key]
        else:
            diff[key] = data[key] - notes_overall[key]
    
    # create and save chart to visualize results
    transformed_data = Visualizer.transform_data(diff)
    figure = Visualizer.create_notes_chart(transformed_data)
    fig = figure['figure']
    Visualizer.save_chart(figure)
    
    # save the data to json
    with open(f'data/bourbons/{file}/difference_from_mean.json', 'w') as outfile:
        json.dump(diff, outfile, indent=4)
        outfile.close()
        
    
        
        
    
    
# with open('get_avg_notes_results.json', 'w') as outfile:
#     json.dump(notes_overall, outfile, indent=4)

# bourbon_name_o = "Elijah Craig Small Batch"

# bourbon_name = bourbon_name_o.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower()

# with open(f'data/bourbons/{bourbon_name}/info.json', 'r') as infile:
#     ec_data = json.load(infile)
#     infile.close()
    
# del ec_data['bourbon_name']

# ec_diff = {}
# for key in ec_data.keys():
#     diff = ec_data[key] - notes_overall[key]
#     # if diff < 0:
#     #     diff_ = f"- {diff}"
#     # else:
#     #     diff_ = f"+ {diff}"
#     # ec_diff[key] = diff_
#     ec_diff[key] = diff
    
# # with open('get_avg_notes_ec.json', 'w') as outfile:
# #     json.dump(ec_diff, outfile, indent=4)

# ec_diff['bourbon_name'] = bourbon_name_o

# from src.__classes__.__visualizer__ import Visualizer

# transformed_data = Visualizer.transform_data(ec_diff)
# figure = Visualizer.create_notes_chart(transformed_data)
# fig = figure['figure']
# fig.show()
# Visualizer.save_chart(figure)