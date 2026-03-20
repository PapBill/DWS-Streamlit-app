import streamlit as st

st.title("🏚 Airbnb Project")

st.write("SFcdcsaccsc")

with st.expander("Dataset Overview"):

 df =pd.read_csv('https://github.com/PapBill/DWS-Streamlit-app/blob/main/dataset.csv')
 st.write("Neapoli Dataset")
 df
