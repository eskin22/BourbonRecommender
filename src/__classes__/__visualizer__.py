
import pandas as pd
import plotly.graph_objects as go
import json
import string

class Visualizer:
    
    def transform_data(data):
        
        bourbon_name = data['bourbon_name']
        del data['bourbon_name']
        
        new_data = {'note':[], 'value':[]}
        for key, val in data.items():
            new_data['note'].append(key)
            new_data['value'].append(val)

        df = pd.DataFrame(new_data)

        # convert the 'value' column to a float representation of percentage
        df['value'] = df['value'].astype(float)

        # Sort the dataframe by 'value' in descending order
        df = df.sort_values(by='value', ascending=True)

        # Create a 'Percentage' column formatted without decimal places and with a percentage sign
        df['Percentage'] = df['value'].apply(lambda x: f"{x*100:.0f}%")

        df['note'] = df['note'] + '  '
        df['note'] = df['note'].astype('category')
        
        return {'bourbon_name': bourbon_name, 'data': df}
        
    
    def create_notes_chart(data):
        
        bourbon_name, df = data['bourbon_name'], data['data']

        fig = go.Figure(data=[
            go.Bar(
                y=df['note'],
                x=df['value'],
                text=df['Percentage'],
                textposition='outside',
                marker_color='#c9f66f',
                orientation='h',
                textfont=dict(
                    family='Segoe UI Semibold',
                    # size=20,
                    color='white'
                ),
                hoverinfo='none'
            )
        ])

        fig.update_layout(
            title_text=f"<b>{bourbon_name}</b>",
            title_font=dict(size=32, family='Segoe UI', color='white'),
            title_x=0.5,
            yaxis=dict(
                showgrid=False, 
                showticklabels=True, 
                tickfont=dict(family='Segoe UI Semibold', color='white'),
                automargin=True
            ),
            xaxis=dict(domain=[0.05, 0.95], showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='#1C1C1C',
            paper_bgcolor='#1C1C1C',
            # margin=dict(t=80),
            width=900,
            height=1200
        )
        
        return {'bourbon_name': bourbon_name, 'figure': fig}
    
    def save_chart(data, fnc):
        
        bourbon_name, fig = data['bourbon_name'], data['figure']
        
        bourbon_name = bourbon_name.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').lower()
        
        fig.write_image(f'data/bourbons/{bourbon_name}/notes_{fnc}.png', scale=10)
        
        # img_bytes = fig.to_image('png')

        # with open(f'data/bourbons/{bourbon_name}/notes_breakdown.png', 'wb') as f:
        #     f.write(img_bytes)
        #     f.close()