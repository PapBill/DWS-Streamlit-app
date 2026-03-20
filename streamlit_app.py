import streamlit as st

st.title("🏚 Airbnb Project")

st.write("SFcdcsaccsc")

with st.expander("Dataset Overview"):
    df = pd.read_csv('https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/dataset.csv')
    st.write("Neapoli Dataset")
    st.write(df)
