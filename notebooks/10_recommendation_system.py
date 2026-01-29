import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors

# Load data
df = pd.read_csv("data/cleaned/master_dataset.csv")

# Use UNIQUE attractions only (CRITICAL)
rec_df = (
    df[["Attraction", "AttractionType"]]
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

# Encode AttractionType
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X = encoder.fit_transform(rec_df[["AttractionType"]])

# Fit Nearest Neighbors model
nn_model = NearestNeighbors(
    n_neighbors=6,          # 1 self + 5 recommendations
    metric="cosine",
    algorithm="brute"
)

nn_model.fit(X)

# Recommendation function
def recommend_attractions(attraction_name, top_n=5):
    if attraction_name not in rec_df["Attraction"].values:
        return "Attraction not found."

    idx = rec_df[rec_df["Attraction"] == attraction_name].index[0]

    distances, indices = nn_model.kneighbors(X[idx].reshape(1, -1))

    recommended_indices = indices[0][1 : top_n + 1]

    return rec_df.iloc[recommended_indices]

# ---- TEST ----
sample = rec_df["Attraction"].iloc[0]
print("Sample attraction:", sample)
print("\nRecommended attractions:")
print(recommend_attractions(sample))
