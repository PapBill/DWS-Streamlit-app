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
    st.session_state.show_inputs = False
    st.session_state.predicted_price = None
      # Hide sidebar

def predict_price():
    st.session_state.predicted_price = 300
    
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

if 'predicted_price' not in st.session_state:
    st.session_state.predicted_price = None

#---------------------------------------------#

# Add background image to the main page
main_page_img = """
    <style>
    [data-testid="stAppViewContainer"],
    [data-testid="stMainContainer"],
    [data-testid="stAppViewContainer"] > div:first-child {
        background-image: url("https://centralmacedoniablob.blob.core.windows.net/portal-content/1Istoriko_kentro_thessalonikis_3.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        min-height: 100vh;
    }

    [data-testid="stAppViewContainer"] .css-1d391kg,
    [data-testid="stAppViewContainer"] .css-1dp5vir {
        background-color: rgba(255, 255, 255, 0.82) !important;
    }
    </style>
    """
st.markdown(main_page_img, unsafe_allow_html=True)

st.title("🏠 Airbnb Project ")
st.write("**My Streamlit app for Aibnb data visualization and price prediction**")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] .css-18e3th9 { /* main content text */
    color: #fdf4d9 !important; /* light sunset text */
    text-shadow: 0 0 8px rgba(255, 130, 40, 0.9);
}
[data-testid="stAppViewContainer"] .stMarkdown h1,
[data-testid="stAppViewContainer"] .stMarkdown h2 {
    color: #ffbb00 !important;
}
[data-testid="stAppViewContainer"] .stMarkdown p {
    color: #ffe7b0 !important;
}
</style>
""", unsafe_allow_html=True)


with st.expander("**Dataset Overview**"):
    df = pd.read_csv('https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/dataset.csv', encoding='latin1')
    st.write("Neapoli Dataset")
    st.write(df)

with st.expander("**Dataset Visualization**"):

    tab1, tab2, tab3, tab4, tab5 =st.tabs(["**Plot1**", "**Plot2**", "**Plot3**", "**Plot4**", "**Plot5**"], on_change="rerun")

    with tab1:
        st.line_chart({"data": [1, 5, 2, 6, 2, 1]})       
    with tab2:
        pass
    with tab3:
        pass
    with tab4:
        pass
    with tab5:
        pass


with st.sidebar:

    # Set sidebar background color with reliable Streamlit selectors
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #ff4500 !important;
            box-shadow: 10px 10px 30px rgba(0, 0, 0, 0.35) !important;
            border: 1px solid rgba(0,0,0,0.12) !important;
            border-radius: 16px !important;
            backface-visibility: hidden;
            transform: translateZ(0px);
        }

        [data-testid="stSidebar"] > div {
            background-color: rgba(255, 165, 0, 0.97) !important;
            background-image: linear-gradient(145deg, #ffb347 0%, #ff4500 100%) !important;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.14) !important;
        }

        [data-testid="stSidebar"] .css-1d391kg,
        [data-testid="stSidebar"] .css-uhf3jo,
        [data-testid="stSidebar"] .css-1d391kg > div {
            background-color: rgba(255, 140, 0, 0.92) !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stButton {
            color: #fff !important;
        }

        [data-testid="stSidebar"] .stButton>button {
            background: linear-gradient(145deg, #ff7e00 0%, #ff4500 100%) !important;
            color: #fff !important;
            border: 1px solid rgba(255,255,255,0.5) !important;
            box-shadow: 0 4px 16px rgba(255, 94, 0, 0.45) !important;
            border-radius: 12px !important;
            padding: 0.45rem 0.9rem !important;
        }

        [data-testid="stSidebar"] .stButton>button:hover {
            background: linear-gradient(145deg, #ff8f33 0%, #ff5722 100%) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("***Do you want to predict a price?***")
    st.button('**Find house**', on_click=show_inputs, key='find_house_button')

    if st.session_state.show_inputs:
           
            st.write("**Please, enter your preferences:**")

            area = st.selectbox(
                "**Area:**",
                ("Kalamaria", "Panorama", "Neapoli Sikies"),
                placeholder="None",
                index = None if st.session_state.area is None else ("Kalamaria", "Panorama", "Neapoli Sikies").index(st.session_state.area),
                key='area',
                help="Select the area you want to stay in")

            guests = st.number_input(
                "**Number of guests:**",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Enter the number of guests (1-10)")

            beds = st.number_input(
                "**Number of beds:**",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Enter the number of beds (1-10)")

            bedrooms = st.number_input(
                "**Number of bedrooms:**",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="If you want to find a Studio, set this to 1")

            baths = st.number_input(
                "**Number of baths:**",
                min_value=1.0,
                max_value=3.0,
                value=1.0,
                step=0.5,
                help="Enter the number of baths (1-3)")
            
            rating = st.slider(
                "**Rating:**",
                min_value=0.0,
                max_value=5.0,
                value=3.0,
                step=0.1,
                help="Select the minimum rating you want for the property (0-5)")
            
            reviews = st.slider(
                "**Number of reviews:**",
                min_value=0,
                max_value=1000,
                value=1,
                step=1,
                help="Enter the minimum number of reviews you want for the property (0-1000)")

            host = st.text_input(
                "**Host name:**",
                placeholder="Enter the host name",
                help="Enter the name of the host you want to find a property from")
           
            isSuperhost = st.checkbox(
                "**Superhost**",
                 help="Check if you want to find a superhost property")

            isFavourite = st.checkbox(
                "**Favourite**",
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
                st.button('Undo', on_click=erase_inputs, key='undo_button')

            with st.container(horizontal_alignment="left"):
                st.text("Your inputs : ")
                st.write("**Area:** ", inputs['area'].iloc[0])
                st.write("**Guests:** ", inputs['guests'].iloc[0])
                st.write("**Beds:** ", inputs['beds'].iloc[0])
                st.write("**Bedrooms:** ", inputs['bedrooms'].iloc[0])
                st.write("**Baths:** ", inputs['baths'].iloc[0])
                st.write("**Rating:** ", inputs['rating'].iloc[0])
                st.write("**Reviews:** ", inputs['reviews'].iloc[0])
                st.write("**Host:** ", inputs['host'].iloc[0])
                st.write("**Superhost:** ", inputs['isSuperhost'].iloc[0])
                st.write("**Favourite:** ", inputs['isFavourite'].iloc[0])
            
            with st.container(horizontal_alignment="center"):    
                st.button('**Predict Price:**', on_click=predict_price, key='predict_button')
                if st.session_state.predicted_price is not None:
                    st.write(f"**The estimated price based on your inputs is : {st.session_state.predicted_price}€**")
