import pandas as pd

df = pd.read_csv("data/cleaned/master_dataset.csv")

# Select features for ML
features = df[[
    "VisitYear",
    "VisitMonth",
    "Continent",
    "Country",
    "Region",
    "AttractionType"
]]

target_regression = df["Rating"]
target_classification = df["VisitMode"]

print(features.head())

from sklearn.preprocessing import OneHotEncoder

categorical_cols = [
    "Continent",
    "Country",
    "Region",
    "AttractionType"
]

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

encoded = encoder.fit_transform(features[categorical_cols])

encoded_df = pd.DataFrame(
    encoded,
    columns=encoder.get_feature_names_out(categorical_cols)
)

numeric_df = features[["VisitYear", "VisitMonth"]].reset_index(drop=True)

X = pd.concat([numeric_df, encoded_df], axis=1)

print("Final feature shape:", X.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X, target_regression, test_size=0.2, random_state=42
)

_, _, y_clf_train, y_clf_test = train_test_split(
    X, target_classification, test_size=0.2, random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)
