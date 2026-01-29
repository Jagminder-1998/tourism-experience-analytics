import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load data
df = pd.read_csv("data/cleaned/master_dataset.csv")

# Select features and target
features = df[[
    "VisitYear",
    "VisitMonth",
    "Continent",
    "Country",
    "Region",
    "AttractionType"
]]

target = df["VisitMode"]

# Encode categorical features
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

# FINAL feature matrix
X = pd.concat([numeric_df, encoded_df], axis=1)

# Train-test split (with stratification)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    target,
    test_size=0.2,
    random_state=42,
    stratify=target
)

# Train classifier
clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
