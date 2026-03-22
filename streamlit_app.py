import streamlit as st
import pandas as pd
import time

#------------------definitions----------------#
def show_inputs():
    st.session_state.show_inputs = True

def erase_inputs():
    st.session_state.include_archived = False
    st.session_state.min_score = 50
    st.session_state.area = None
    st.session_state.show_inputs = False  # Hide sidebar

    
#---------------------------------------------#
#---------------Initializations---------------#
if 'show_inputs' not in st.session_state:
        st.session_state.show_inputs = False

if 'include_archived' not in st.session_state:

    st.session_state.include_archived = False
if 'min_score' not in st.session_state:

    st.session_state.min_score = 50
if 'area' not in st.session_state:

    st.session_state.area = None

#---------------------------------------------#

st.title("🏚 Airbnb Project")

st.write("My Streamlit app for Aibnb data visualization and price prediction")

with st.expander("Dataset Overview"):
    df = pd.read_csv('https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/dataset.csv', encoding='latin1')
    st.write("Neapoli Dataset")
    st.write(df)

with st.expander("Dataset Visualization"):

    tab1, tab2, tab3, tab4, tab5 =st.tabs(["Plot1", "Plot2", "Plot3", "Plot4", "Plot5"], on_change="rerun")

    with tab1:
        st.line_chart({"data": [1, 5, 2, 6, 2, 1]})    
    with tab1:
        st.line_chart({"data": [1, 5, 2, 6]})   
    with tab2:
        pass
    with tab3:
        pass
    with tab4:
        pass
    with tab5:
        pass


with st.sidebar:
    st.header("Do you want to predict a price?")
    st.button('Find house', on_click=show_inputs)
    if st.session_state.show_inputs:
           
            st.write("Please, enter your preferences:")

            area = st.selectbox(
                "Are:",
                ("Kalamaria", "Panorama", "Neapoli"),
                placeholder="None",
                index = None if st.session_state.area is None else ("Kalamaria", "Panorama", "Neapoli").index(st.session_state.area),
                key='area',
                help="Select the area you want to stay in")

            guests = st.number_input(
                "Number of guests:",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Enter the number of guests (1-10)")

            beds = st.number_input(
                "Number of beds:",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Enter the number of beds (1-10)")

            bedrooms = st.number_input(
                "Number of bedrooms:",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="If you want to find a Studio, set this to 1")

            baths = st.number_input(
                "Number of baths:",
                min_value=1.0,
                max_value=3.0,
                value=1.0,
                step=0.5,
                help="Enter the number of baths (1-3)")
            
            rating = st.slider(
                "Rating:",
                min_value=0.0,
                max_value=5.0,
                value=3.0,
                step=0.1,
                help="Select the minimum rating you want for the property (0-5)")
            
            reviews = st.slider(
                "Number of reviews:",
                min_value=0,
                max_value=1000,
                value=1,
                step=1,
                help="Enter the minimum number of reviews you want for the property (0-1000)")

            host = st.text_input(
                "Host name:",
                placeholder="Enter the host name",
                help="Enter the name of the host you want to find a property from")
           
            isSuperhost = st.checkbox(
                "Superhost",
                 help="Check if you want to find a superhost property")

            isFavourite = st.checkbox(
                "Favourite",
                 help="Check if you want to find a property that is marked as favourite by users")

            data ={
                "area": area,
                "guests": guests,
                "beds": beds,
                "bedrooms": bedrooms,
                "baths": baths,
                "rating": rating,
                "reviews": reviews,
                "host": host,
                "isSuperhost": isSuperhost,
                "isFavourite": isFavourite
            }
            inputs = pd.DataFrame(data,index=[0])
                
            with st.container(horizontal_alignment="center"):    
                st.button('Undo', on_click=erase_inputs)

            
                    
                
                    
                    
        


