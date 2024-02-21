# add the file to the sys.path to allow execution from root directory
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
import plotly.graph_objects as go
import json

with open('data/bourbons/blantons_original_single_barrel/info.json', 'r') as infile:
    data = json.load(infile)
    infile.close()
    
del data['bourbon_name']
    
new_data = {'note':[], 'value':[]}
for key, val in data.items():
    new_data['note'].append(key)
    new_data['value'].append(val)

df = pd.DataFrame(new_data)

# Convert the 'value' column to a float representation of percentage (e.g., 0.7 for 70%)
df['value'] = df['value'].astype(float)

# Sort the dataframe by 'value' in descending order
df = df.sort_values(by='value', ascending=True)

# Create a 'Percentage' column formatted without decimal places and with a percentage sign
df['Percentage'] = df['value'].apply(lambda x: f"{x*100:.0f}%")

df['note'] = df['note'] + '  '
df['note'] = df['note'].astype('category')

# Create the bar chart with horizontal bars
fig = go.Figure(data=[
    go.Bar(
        y=df['note'],  # Categories on the y-axis
        x=df['value'],  # Values on the x-axis
        text=df['Percentage'],  # Data labels
        textposition='outside',  # Position the data labels automatically
        marker_color='#c9f66f',  # Bar color
        orientation='h',  # Horizontal bars
        textfont=dict(
            family='Segoe UI Semibold',
            # size=20,
            color='white'
        ),
        hoverinfo='none'  # Disable hover labels
    )
])

# Customize the layout
fig.update_layout(
    title_text="<b>Blanton's Original Single Barrel</b>",  # Chart title
    title_font=dict(size=32, family='Segoe UI', color='white'),  # Title font properties
    title_x=0.5,
    yaxis=dict(
        showgrid=False, 
        showticklabels=True, 
        tickfont=dict(family='Segoe UI Semibold', color='white'),
        automargin=True  # Automatically adjust margin to fit tick labels
    ),
    xaxis=dict(domain=[0.2, 0.8], showgrid=False, zeroline=False, showticklabels=False),  # Customize X-axis
    plot_bgcolor='#1C1C1C',  # Transparent plot background
    paper_bgcolor='#1C1C1C',  # Transparent figure background
    margin=dict(l=50, r=10, t=80, b=50),
    # width=600,
    # height=900
)

# Show the figure
fig.show()

print("saving...")

img_bytes = fig.to_image('png')
# img_bytes = pio.to_image(fig, format='png')

with open('demo_chart.png', 'wb') as f:
    f.write(img_bytes)
    f.close()
print("saved.")