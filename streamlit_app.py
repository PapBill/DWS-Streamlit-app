import streamlit as st
import pandas as pd

st.title("🏚 Airbnb Project")

st.write("       My Streamlit app for Aibnb data visualization and price prediction")

with st.expander("Dataset Overview"):
    df = pd.read_csv('https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/dataset.csv', encoding='latin1')
    st.write("Neapoli Dataset")
    st.write(df)
