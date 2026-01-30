import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Tourism Experience Analytics",
    layout="wide"
)

st.title("🌍 Tourism Experience Analytics")
st.write("Visit Mode Prediction & Attraction Recommendation System")

# ==================================================
# LOAD DATA (CACHED – SAFE)
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned/master_dataset.csv")

df = load_data()

# ==================================================
# HELPER FUNCTION
# ==================================================
def clean_unique(series):
    return sorted(series.dropna().astype(str).unique())

# ==================================================
# TRAIN MODEL (CACHED – DF NOT HASHED)
# ==================================================
@st.cache_resource
def train_visit_mode_model(_df):

    features = _df[
        ["VisitYear", "VisitMonth", "Continent", "Country", "Region", "AttractionType"]
    ].dropna()

    target = _df.loc[features.index, "VisitMode"]

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

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

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X, target)

    return model, encoder, encoded_df.columns

model, encoder, feature_columns = train_visit_mode_model(df)

# ==================================================
# SIDEBAR INPUTS
# ==================================================
st.sidebar.header("User Input")

visit_year = st.sidebar.selectbox(
    "Visit Year",
    sorted(df["VisitYear"].dropna().unique())
)

visit_month = st.sidebar.selectbox(
    "Visit Month",
    sorted(df["VisitMonth"].dropna().unique())
)

continent = st.sidebar.selectbox(
    "Continent",
    clean_unique(df["Continent"])
)

country = st.sidebar.selectbox(
    "Country",
    clean_unique(df["Country"])
)

region = st.sidebar.selectbox(
    "Region",
    clean_unique(df["Region"])
)

attraction_type = st.sidebar.selectbox(
    "Attraction Type",
    clean_unique(df["AttractionType"])
)

# ==================================================
# VISIT MODE PREDICTION
# ==================================================
st.subheader("🧳 Predicted Visit Mode")

user_input = pd.DataFrame([{
    "VisitYear": visit_year,
    "VisitMonth": visit_month,
    "Continent": continent,
    "Country": country,
    "Region": region,
    "AttractionType": attraction_type
}])

user_encoded = encoder.transform(
    user_input[["Continent", "Country", "Region", "AttractionType"]]
)

user_features = pd.concat(
    [
        user_input[["VisitYear", "VisitMonth"]].reset_index(drop=True),
        pd.DataFrame(user_encoded, columns=feature_columns)
    ],
    axis=1
)

predicted_visit_mode = model.predict(user_features)[0]
st.success(predicted_visit_mode)

# ==================================================
# RECOMMENDATION SYSTEM (AUTO, STABLE)
# ==================================================
st.subheader("🏖️ Recommended Attractions")

recommendations = (
    df[df["AttractionType"] == attraction_type]
    [["Attraction", "AttractionType"]]
    .dropna()
    .drop_duplicates()
    .head(5)
)

if recommendations.empty:
    st.warning("No recommendations available for this attraction type.")
else:
    # Convert to pure Python objects to avoid Arrow / LargeUtf8
    st.table(recommendations.astype(str).to_dict(orient="records"))
