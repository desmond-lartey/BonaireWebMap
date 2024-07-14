import streamlit as st
import os
from math import ceil
import pandas as pd

# Function to get the project root directory
def get_project_root():
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, os.pardir)

# Function to load all image files from the Maps directory
def load_image_files_from_directory(directory="Maps", extensions=("jpg", "jpeg", "png", "gif")):
    project_root = get_project_root()
    directory_path = os.path.join(project_root, directory)
    try:
        if os.path.exists(directory_path):
            return [f for f in os.listdir(directory_path) if f.lower().endswith(extensions)]
        else:
            st.error(f"Directory not found at {directory_path}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Load files from the Maps directory
image_files = load_image_files_from_directory()

def initialize(files):    
    df = pd.DataFrame({'file': files,
                       'incorrect': [False] * len(files),
                       'label': [''] * len(files)})
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
    batch_size = st.select_slider("Batch size:", range(100, 110))
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
        st.image(os.path.join(get_project_root(), "Maps", image), caption='ToWalkto')
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
st.write('## Maps and Charts')
cols = st.columns(len(image_files))
for i, image_file in enumerate(image_files):
    with cols[i]:
        st.image(os.path.join(get_project_root(), "Maps", image_file), caption=f'{image_file}')
