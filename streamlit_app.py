import streamlit as st
import pandas as pd

st.title("🏚 Airbnb Project")

st.write("ABC")

with st.expander("Dataset Overview"):
    df = pd.read_csv('https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/dataset.csv')
    st.write("Neapoli Dataset")
    st.write(df)
