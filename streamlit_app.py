import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import time
from io import StringIO
import requests
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

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
   
#---------------------------------------------#
#---------------Initializations---------------#
if 'show_inputs' not in st.session_state:
        st.session_state.show_inputs = False

if 'include_archived' not in st.session_state:

    st.session_state.include_archived = False
if 'min_score' not in st.session_state:

    st.session_state.min_score = 50
if 'region' not in st.session_state:

    st.session_state.area = None


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

st.title(":streamlit: Airbnb Project ")
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
    df1, df2 = st.tabs(["**Raw Dataset**", "**Cleaned Dataset**"], on_change="rerun")

    with df1:
        url1 = "https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/Combined_datasets.csv"
        response = requests.get(url1)
        response.encoding = "utf-8"
        df = pd.read_csv(StringIO(response.text))
        st.write(df)
    with df2:
        url2 = "https://raw.githubusercontent.com/PapBill/DWS-Streamlit-app/main/clean_dataset.csv"
        response = requests.get(url2)
        response.encoding = "utf-8"
        final_df = pd.read_csv(StringIO(response.text))
        st.write(final_df)
    

with st.expander("**Dataset Visualization**"):

    tab1, tab2, tab3, tab4, tab5, tab6 =st.tabs(["**Property Types**", "**Top10**", "**Bottom10**", "**Correlations**", "**Location Stats**", "**Map**"], on_change="rerun")

    with tab1:

        avg_price_per_property_type = final_df.groupby('property_type')['avg_price_per_night_estimate'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        plot = sns.barplot(data=avg_price_per_property_type, x='property_type', y="avg_price_per_night_estimate", palette='viridis')
        plt.title('Average Price per Property Type')
        plt.xlabel('Property Type')
        plt.ylabel('Average Price per Night')
        plt.xticks(rotation=45)
        st.pyplot(plot.figure)

    with tab2:

        top10 = final_df.sort_values(by=["review_index", "num_reviews"], ascending=[False, False]).head(10)
        st.text("Top-10 rated stays")
        st.write(top10)

    with tab3:

        bottom10 = final_df.sort_values(by=["review_index", "num_reviews"], ascending=[True, True]).head(10)
        st.text("Bottom-10 rated stays")
        st.write(bottom10)

    with tab4:
    
        corr_cols = ["price_total", "guests", "beds", "bedrooms", "baths", "review_index", "num_reviews"]
        corr = final_df[corr_cols].corr()

        plt.figure(figsize=(10, 6))
        var_corr = sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Correlation Matrix of Main Airbnb Variables")
        st.pyplot(var_corr.figure)

    with tab5:

        plt.figure(figsize=(8, 5))
        price_hist = sns.histplot(final_df["price_total"],bins=30, kde=True)
        plt.title("Distribution of Total Price")
        plt.xlabel("Price Total")
        st.pyplot(price_hist.figure)

        plt.figure(figsize=(8, 5))
        price_box = sns.boxplot(data=final_df, x="region", y="price_total", hue="region", palette="Set2")
        plt.title("Price Distribution by Region")
        plt.xticks(rotation=20)
        st.pyplot(price_box.figure)

        plt.figure(figsize=(8, 5))
        region_count = sns.countplot(data=final_df, x="region",palette="Set1")
        plt.title("Number of Listings per Region")
        plt.xticks(rotation=20)
        st.pyplot(region_count.figure)

        avg_price = final_df.groupby("region", as_index=False)["price_total"].mean()

        plt.figure(figsize=(8, 5))
        avg_price_bar = sns.barplot(data=avg_price, x="region", y="price_total", palette="pastel6")
        plt.title("Average Price per Region")
        plt.xticks(rotation=20)
        st.pyplot(avg_price_bar.figure)

        plt.figure(figsize=(8, 5))
        review_hist = sns.histplot(final_df["review_index"], bins=20, kde=True)
        plt.title("Distribution of Review Scores")
        plt.xlabel("Review Index")
        st.pyplot(review_hist.figure)

        plt.figure(figsize=(8, 5))
        guests_scatter = sns.scatterplot(data=final_df, x="guests", y="price_total", hue="guests", palette="Set2")
        plt.title("Price vs Guests Capacity")
        st.pyplot(guests_scatter.figure)

        plt.figure(figsize=(8, 5))
        review_scatter = sns.scatterplot(data=final_df, x="review_index", y="price_total", hue="review_index", palette="coolwarm")
        plt.title("Price vs Review Score")
        st.pyplot(review_scatter.figure)

        plt.figure(figsize=(8, 5))
        host_box = sns.boxplot(data=final_df, x="superhost_binary", y="price_total", palette="Set3")
        plt.title("Price by Superhost Status")
        plt.xticks([0, 1], ["No", "Yes"])
        st.pyplot(host_box.figure)

        plt.figure(figsize=(8, 5))
        score_scatter = sns.scatterplot(data=final_df, x="num_reviews", y="review_index", hue="review_index", palette="viridis")
        plt.title("Number of Reviews vs Review Score")
        st.pyplot(score_scatter.figure)

        eng_cols = [
            "price_total", "price_per_guest", "beds_per_guest",
            "bedrooms_per_guest", "review_index", "num_reviews"
        ]

        plt.figure(figsize=(9, 6))
        features = sns.heatmap(final_df[eng_cols].corr(), annot=True, cmap="viridis")
        plt.title("Correlation of Engineered Features")
        st.pyplot(features.figure)

    with tab6:

        map_df = final_df.dropna(subset=["latitude", "longitude"]).copy()

        m = folium.Map(
        location=[map_df["latitude"].mean(), map_df["longitude"].mean()],
        zoom_start=11
        )

        for _, row in map_df.iterrows():
            popup_text = f"""
            Region: {row['region']}<br>
            Price: €{row['price_total']}<br>
            Review: {row['review_index']}<br>
            Reviews: {row['num_reviews']}
            """
        st_folium(m, width=700, height=500)

    

    
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

            if "region" not in st.session_state:
                st.session_state.region = 'Kalamaria'
            region = st.selectbox(
                "**Region:**",
                ("Kalamaria", "Panorama", "Neapoli Sikies"),
                key='region',
                help="Select the region you want to stay in")

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
            
            review_index = st.slider(
                "**Rating:**",
                min_value=0.0,
                max_value=5.0,
                value=3.0,
                step=0.1,
                help="Select the minimum rating you want for the property (0-5)")
            
            num_reviews = st.slider(
                "**Number of reviews:**",
                min_value=0,
                max_value=1000,
                value=1,
                step=1,
                help="Enter the minimum number of reviews you want for the property (0-1000)")
           
            superhost_binary = st.checkbox(
                "**Superhost**",
                 help="Check if you want to find a superhost property")

            favourite = st.checkbox(
                "**Favourite**",
                 help="Check if you want to find a property that is marked as favourite by users")

            premium_host = st.checkbox(
                "**Premium Host**",
                 help="Check if you want to find a property that is marked as premium host by users")
            


            data ={
                "region": region,
                "guests": guests,
                "bedrooms": bedrooms,
                "beds": beds,
                "baths": baths,
                "superhost_binary": superhost_binary,
                "favourite": favourite,
                "review_index": review_index,
                "num_reviews": num_reviews,
                "beds_per_guest": beds/guests,
                "bedrooms_per_guest": bedrooms/guests,
                "has_reviews": 1 if num_reviews > 0 else 0,
                "high_capacity": 1 if guests >= 4 else 0,
                "premium_host": premium_host
                
            }
            inputs = pd.DataFrame(data,index=[0])   
                   
            with st.container(horizontal_alignment="center"):    
                st.button('Undo', on_click=erase_inputs, key='undo_button')

            with st.container(horizontal_alignment="left"):
                st.subheader("Your inputs : ")
                st.write("**Region:** ", inputs['region'].iloc[0])
                st.write("**Guests:** ", inputs['guests'].iloc[0])
                st.write("**Beds:** ", inputs['beds'].iloc[0])
                st.write("**Bedrooms:** ", inputs['bedrooms'].iloc[0])
                st.write("**Baths:** ", inputs['baths'].iloc[0])
                st.write("**Rating:** ", inputs['review_index'].iloc[0])
                st.write("**Reviews:** ", inputs['num_reviews'].iloc[0])
                st.write("**Superhost:** ", inputs['superhost_binary'].iloc[0])
                st.write("**Favourite:** ", inputs['favourite'].iloc[0])
                st.write("**Premium Host:** ", inputs['premium_host'].iloc[0])
                

            with st.container(horizontal_alignment="center"):      

                    features = [
                         "region",
                        "guests",
                        "bedrooms",
                        "beds",
                        "baths",
                        "superhost_binary",
                        "favourite",
                        "review_index",
                        "num_reviews",
                        "beds_per_guest",
                        "bedrooms_per_guest",
                        "has_reviews",
                        "high_capacity",
                        "premium_host"
                    ]

                    for col in features:
                        inputs[col] = pd.to_numeric(inputs[col], errors="coerce")
                        final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

                    inputs["region"] = inputs["region"].astype(str).str.strip().str.lower()
                    final_df["region"] = final_df["region"].astype(str).str.strip().str.lower()

                    # Train-Test split
                    X = final_df[features]
                    y = final_df["avg_price_per_night_estimate"]

                    X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.25, random_state=42)

                    categorical_features = ["region"]
                    numeric_features = [col for col in features if col not in categorical_features]

                    preprocessor = ColumnTransformer(
                        transformers=[
                            ("num", Pipeline([
                                ("imputer", SimpleImputer(strategy="median"))
                            ]), numeric_features),

                            ("cat", Pipeline([
                                ("imputer", SimpleImputer(strategy="most_frequent")),
                                ("onehot", OneHotEncoder(handle_unknown="ignore"))
                            ]), categorical_features)
                        ]
                    )

                    gb_pipeline = Pipeline([
                        ("preprocessor", preprocessor),
                        ("model", GradientBoostingRegressor(
                            n_estimators=300,
                            learning_rate=0.05,
                            max_depth=3,
                            random_state=42
                        ))
                    ])

                    gb_pipeline.fit(X_train, y_train)
                    gb_pred = gb_pipeline.predict(inputs)

                    st.subheader(f"The estimated price is :")
                    st.success(str(gb_pred[0].round(2)) + " € per night")
