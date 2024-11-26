# app.py

import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd
import requests

model_filename = 'best_model.joblib'

if not os.path.exists(model_filename):
    with st.spinner('Downloading model...'):
        url = 'https://github.com/Samuel-Brasil/M.A.R.I.A./releases/download/v1.3/best_model.joblib'
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(model_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            st.success('Model downloaded successfully.')
        else:
            st.error('Failed to download the model.')
            st.stop()

# Load the model
model = joblib.load(model_filename)

# Load the trained model
#model = joblib.load('best_model.joblib')

# Define a function for prediction
def predict_decision(input_data):
    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])
    # Make prediction
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)
    return prediction[0], prediction_proba[0][1]

# Streamlit app layout
st.title('M.A.R.I.A.')
st.write('# Modelagem da Avaliação de Risco com Inteligência Artificial')
st.write('Violence Risk Prediction App')

st.write("""
This app predicts whether a protective measure will be granted based on the input data.
""")

# Collect user input
st.header('Enter the Details:')

# Assuming these are the features required by the model
# Replace with actual feature names and appropriate input methods
input_data = {}

input_data['idade_vit'] = st.number_input('Victim Age', min_value=0, max_value=120, value=30)
input_data['idade_agr'] = st.number_input('Aggressor Age', min_value=0, max_value=120, value=35)

# For boolean inputs, use checkboxes
input_data['historico_ameaca'] = st.checkbox('History of Threats')
input_data['agr_doenca_mental'] = st.checkbox('Aggressor has Mental Illness')
input_data['agr_alcool_drogas'] = st.checkbox('Aggressor Abuses Alcohol or Drugs')

# Continue for all other features
# For categorical features, use selectbox or multiselect
# For the cumulative response features, you need to provide multiselect options

# Example for a categorical feature encoded via one-hot encoding
etnia_options = ['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena', 'Não informada']
selected_etnia = st.selectbox('Ethnicity', etnia_options)

# Convert the selected ethnicity into the appropriate one-hot encoded format
for etnia in etnia_options:
    input_data[f'etnia_{etnia}'] = 1 if selected_etnia == etnia else 0

# Example for cumulative response features
agressoes_options = ['Empurrões', 'Tapas', 'Socos', 'Chutes', 'Estrangulamento', 'Puxões de cabelo']
selected_agressoes = st.multiselect('Types of Aggressions', agressoes_options)

# Convert the selected aggressions into binary features
for ag in agressoes_options:
    input_data[f'agressoes_{ag}'] = 1 if ag in selected_agressoes else 0

# Once all inputs are collected, create a predict button
if st.button('Predict'):
    prediction, probability = predict_decision(input_data)
    if prediction:
        st.success(f"The model predicts that the protective measure will be GRANTED with a probability of {probability:.2f}.")
    else:
        st.error(f"The model predicts that the protective measure will be DENIED with a probability of {1 - probability:.2f}.")
