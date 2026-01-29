import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Tourism Experience Analytics", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/cleaned/master_dataset.csv")

st.title("🌍 Tourism Experience Analytics")
st.write("Prediction & Recommendation System for Tourism Platforms")

# ---------------- SIDEBAR ----------------
st.sidebar.header("User Input")

visit_year = st.sidebar.selectbox("Visit Year", sorted(df["VisitYear"].unique()))
visit_month = st.sidebar.selectbox("Visit Month", sorted(df["VisitMonth"].unique()))
continent = st.sidebar.selectbox("Continent", df["Continent"].unique())
country = st.sidebar.selectbox("Country", df["Country"].unique())
region = st.sidebar.selectbox("Region", df["Region"].unique())
attraction_type = st.sidebar.selectbox("Attraction Type", df["AttractionType"].unique())

# ---------------- VISIT MODE PREDICTION ----------------
features = df[[
    "VisitYear",
    "VisitMonth",
    "Continent",
    "Country",
    "Region",
    "AttractionType"
]]

target = df["VisitMode"]

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded = encoder.fit_transform(
    features[["Continent", "Country", "Region", "AttractionType"]]
)

encoded_df = pd.DataFrame(
    encoded,
    columns=encoder.get_feature_names_out(
        ["Continent", "Country", "Region", "AttractionType"]
    )
)

numeric_df = features[["VisitYear", "VisitMonth"]].reset_index(drop=True)
X = pd.concat([numeric_df, encoded_df], axis=1)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X, target)

user_input = pd.DataFrame([{
    "VisitYear": visit_year,
    "VisitMonth": visit_month,
    "Continent": continent,
    "Country": country,
    "Region": region,
    "AttractionType": attraction_type
}])

user_encoded = encoder.transform(user_input[["Continent","Country","Region","AttractionType"]])
user_df = pd.concat([
    user_input[["VisitYear","VisitMonth"]].reset_index(drop=True),
    pd.DataFrame(user_encoded, columns=encoded_df.columns)
], axis=1)

predicted_mode = clf.predict(user_df)[0]

st.subheader("🧳 Predicted Visit Mode")
st.success(predicted_mode)

# ---------------- RECOMMENDATION SYSTEM ----------------
st.subheader("🏖️ Recommended Attractions")

rec_df = (
    df[["Attraction", "AttractionType"]]
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_rec = enc.fit_transform(rec_df[["AttractionType"]])

nn = NearestNeighbors(n_neighbors=6, metric="cosine")
nn.fit(X_rec)

selected_attr = st.selectbox("Choose an attraction", rec_df["Attraction"].values)

idx = rec_df[rec_df["Attraction"] == selected_attr].index[0]
_, indices = nn.kneighbors(X_rec[idx].reshape(1, -1))

recommendations = rec_df.iloc[indices[0][1:]]

st.dataframe(recommendations)
