import pandas as pd

df = pd.read_csv("data/cleaned/master_dataset.csv")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nMissing values:\n", df.isna().sum())
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(6,4))
sns.histplot(df["Rating"], bins=5, kde=True)
plt.title("Distribution of Attraction Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="VisitMode")
plt.title("Distribution of Visit Modes")
plt.xticks(rotation=30)
plt.show()
plt.figure(figsize=(8,5))
sns.countplot(
    data=df,
    y="AttractionType",
    order=df["AttractionType"].value_counts().index
)
plt.title("Popularity of Attraction Types")
plt.show()
