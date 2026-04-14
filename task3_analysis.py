import pandas as pd
import numpy as np
import os

# ---------------- LOAD ---------------- #
filename = "data/trends_clean.csv"

try:
    df = pd.read_csv(filename)
    print(f"Loaded Data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    df = pd.DataFrame()

if df.empty:
    print("No data to analyze.")
    exit()

print("\nFirst 5 rows:")
print(df.head())

# ---------------- BASIC STATS ---------------- #
print("\n----- Basic Stats -----")

# Ensure numeric safety
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0)

print(f"Average Score: {df['score'].mean():.2f}")
print(f"Average Comments: {df['num_comments'].mean():.2f}")

# ---------------- NUMPY STATS ---------------- #
print("\n----- Numpy Stats -----")

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()
categories = df["category"].astype(str).to_numpy()
titles = df["title"].astype(str).to_numpy()

print(f"Mean Score: {np.mean(scores):.2f}")
print(f"Median Score: {np.median(scores):.2f}")
print(f"Std Deviation: {np.std(scores):.2f}")
print(f"Max Score: {np.max(scores)}")
print(f"Min Score: {np.min(scores)}")

# ---------------- CATEGORY ANALYSIS ---------------- #
category, counts = np.unique(categories, return_counts=True)
max_cat_index = np.argmax(counts)

print(f"\nTop Category: {category[max_cat_index]} ({counts[max_cat_index]} stories)")

# ---------------- TOP STORIES ---------------- #
max_comment_index = np.argmax(comments)
max_score_index = np.argmax(scores)

print(f"\nMost Commented Story:\n{titles[max_comment_index]} ({comments[max_comment_index]} comments)")
print(f"\nHighest Scored Story:\n{titles[max_score_index]} ({scores[max_score_index]} points)")

# ---------------- FEATURE ENGINEERING ---------------- #

# Avoid division by zero safely
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if above average score
avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score

# Trending score (better metric)
df["trend_score"] = (
    df["score"] * 0.6 +
    df["num_comments"] * 0.4
)

# Normalize trend score (0–1 scale)
df["trend_score_norm"] = (
    (df["trend_score"] - df["trend_score"].min()) /
    (df["trend_score"].max() - df["trend_score"].min() + 1e-9)
)

# ---------------- EXTRA INSIGHTS ---------------- #

print("\nTop 5 Trending Stories:")
print(df.sort_values(by="trend_score", ascending=False)[["title", "trend_score"]].head())

print("\nAverage Engagement per Category:")
print(df.groupby("category")["engagement"].mean().round(3))

# ---------------- SAVE ---------------- #

os.makedirs("data", exist_ok=True)

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

if os.path.exists(output_file):
    print(f"\nSaved data to {output_file}")
else:
    print("\nSave failed!")
