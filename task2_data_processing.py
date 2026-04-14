import pandas as pd
import os

# ---------------- LOAD ---------------- #
filename = "data/trends_20260411.json"

try:
    df = pd.read_json(filename)
    print(f"Loaded {df.shape[0]} stories from {filename}")
except Exception as e:
    print("Error loading file:", e)
    df = pd.DataFrame()

if df.empty:
    print("No data to process.")
    exit()

# ---------------- CLEAN ---------------- #

# Remove duplicates
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {df.shape[0]}")

# Remove nulls safely
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {df.shape[0]}")

# Fix data types
df["post_id"] = df["post_id"].astype("int64", errors="ignore")
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype("int64")
df["num_comments"] = pd.to_numeric(df.get("num_comments", 0), errors="coerce").fillna(0).astype("int64")

# Filter low-quality posts
df = df[df["score"] > 5]
print(f"After removing low scores: {df.shape[0]}")

# Clean text
df["title"] = df["title"].astype(str).str.strip()

# Optional: remove very short titles
df = df[df["title"].str.len() > 10]

# ---------------- SAVE ---------------- #

# Fix directory creation (bug fix)
os.makedirs("data", exist_ok=True)

output_csv = "data/trends_clean.csv"
output_json = "data/trends_clean.json"

df.to_csv(output_csv, index=False)
df.to_json(output_json, orient="records", indent=4)

print(f"Saved {df.shape[0]} rows to {output_csv} and {output_json}")

# ---------------- ANALYSIS ---------------- #

print("\nStories per category:")
print(df["category"].value_counts())

print("\nTop 5 highest scored stories:")
print(df.sort_values(by="score", ascending=False)[["title", "score"]].head())

print("\nAverage score per category:")
print(df.groupby("category")["score"].mean().round(2))
