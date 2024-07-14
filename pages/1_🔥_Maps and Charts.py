import streamlit as st
from os import listdir
from math import ceil
import pandas as pd

# Set the directory for images, maps, and charts
image_directory = r'C:\Users\Gebruiker\Desktop\My Lab\Bonaire\BonaireWebMap\Maps\Walkingtime.png'
map_directory = 'images/maps'
chart_directory = 'images/charts'

# List files in each directory
image_files = listdir(image_directory)
map_files = listdir(map_directory)
chart_files = listdir(chart_directory)

def initialize(files):    
    df = pd.DataFrame({'file':files,
                       'incorrect':[False]*len(files),
                       'label':['']*len(files)})
    df.set_index('file', inplace=True)
    return df

# Initialize session state
if 'df' not in st.session_state:
    df = initialize(image_files)
    st.session_state.df = df
else:
    df = st.session_state.df 

controls = st.columns(3)
with controls[0]:
    batch_size = st.select_slider("Batch size:", range(10, 110, 10))
with controls[1]:
    row_size = st.select_slider("Row size:", range(1, 6), value=5)
num_batches = ceil(len(image_files) / batch_size)
with controls[2]:
    page = st.selectbox("Page", range(1, num_batches + 1))

def update(image, col): 
    df.at[image, col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
        st.session_state[f'label_{image}'] = ''
        df.at[image, 'label'] = ''

batch = image_files[(page - 1) * batch_size: page * batch_size]

grid = st.columns(row_size)
col = 0
for image in batch:
    with grid[col]:
        st.image(f'{image_directory}/{image}', caption='bike')
        st.checkbox("Incorrect", key=f'incorrect_{image}', 
                    value=df.at[image, 'incorrect'], 
                    on_change=update, args=(image, 'incorrect'))
        if df.at[image, 'incorrect']:
            st.text_input('New label:', key=f'label_{image}', 
                          value=df.at[image, 'label'],
                          on_change=update, args=(image, 'label'))
        else:
            st.write('##')
            st.write('##')
            st.write('###')
    col = (col + 1) % row_size

st.write('## Corrections')
st.dataframe(df[df['incorrect'] == True])

# Display maps and charts
st.write('## Maps')
map_cols = st.columns(len(map_files))
for i, map_file in enumerate(map_files):
    with map_cols[i]:
        st.image(f'{map_directory}/{map_file}', caption=f'Map {i+1}')

st.write('## Charts')
chart_cols = st.columns(len(chart_files))
for i, chart_file in enumerate(chart_files):
    with chart_cols[i]:
        st.image(f'{chart_directory}/{chart_file}', caption=f'Chart {i+1}')
