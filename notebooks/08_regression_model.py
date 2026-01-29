import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Load prepared data
df = pd.read_csv("data/cleaned/master_dataset.csv")

# Recreate features & target (same as feature engineering)
features = df[[
    "VisitYear",
    "VisitMonth",
    "Continent",
    "Country",
    "Region",
    "AttractionType"
]]

target = df["Rating"]

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded = encoder.fit_transform(features[["Continent","Country","Region","AttractionType"]])
encoded_df = pd.DataFrame(
    encoded,
    columns=encoder.get_feature_names_out(["Continent","Country","Region","AttractionType"])
)

numeric_df = features[["VisitYear","VisitMonth"]].reset_index(drop=True)
X = pd.concat([numeric_df, encoded_df], axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X, target, test_size=0.2, random_state=42
)

# Train model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Predict
y_pred = lr.predict(X_test)

# Evaluate
import numpy as np
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

r2 = r2_score(y_test, y_pred)

print("Linear Regression Results")
print("RMSE:", rmse)
print("R2 Score:", r2)

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

r2_rf = r2_score(y_test, y_pred_rf)

print("\nRandom Forest Regression Results")
print("RMSE:", rmse_rf)
print("R2 Score:", r2_rf)
