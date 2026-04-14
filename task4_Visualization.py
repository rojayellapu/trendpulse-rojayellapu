import pandas as pd
import matplotlib.pyplot as plt
import os
# ---------------- LOAD ---------------- #
file_path = "data/trends_analysed.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    df = pd.DataFrame()

if df.empty:
    print("No data available.")
    exit()

# Ensure numeric safety
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0)

# ---------------- SETUP ---------------- #
os.makedirs("outputs", exist_ok=True)

plt.style.use("ggplot")

# ---------------- CHART 1: TOP STORIES ---------------- #
top_stories = df.sort_values("score", ascending=False).head(10).copy()
top_stories["title"] = top_stories["title"].astype(str).str.slice(0, 60)
top_stories = top_stories[::-1]  # reverse for better barh display

plt.figure(figsize=(12, 8))
plt.barh(top_stories["title"], top_stories["score"], color="skyblue")
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=300)
plt.close()

# ---------------- CHART 2: CATEGORY DISTRIBUTION ---------------- #
cat = df["category"].value_counts()

plt.figure(figsize=(10, 6))
plt.bar(cat.index, cat.values, color="coral")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=300)
plt.close()

# ---------------- CHART 3: SCATTER ---------------- #
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8, 6))
plt.scatter(popular["score"], popular["num_comments"], 
            label="Popular", alpha=0.7, color="green")
plt.scatter(not_popular["score"], not_popular["num_comments"], 
            label="Not Popular", alpha=0.5, color="red")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments (Popularity Analysis)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=300)
plt.close()

# ---------------- DASHBOARD ---------------- #
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Top stories
axes[0].barh(top_stories["title"], top_stories["score"], color="skyblue")
axes[0].set_title("Top Stories")

# Categories
axes[1].bar(cat.index, cat.values, color="coral")
axes[1].set_title("Categories")
axes[1].tick_params(axis='x', rotation=30)

# Scatter
axes[2].scatter(popular["score"], popular["num_comments"], 
                label="Popular", alpha=0.7, color="green")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], 
                label="Not Popular", alpha=0.5, color="red")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].set_title("Popularity")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard", fontsize=16)
plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=300)
plt.close()

print("All charts saved in 'outputs/' folder ")

# Example chart
df['category'].value_counts().plot(kind='bar')

plt.title("Top Categories")

# SAVE IMAGE (IMPORTANT)
plt.savefig("outputs/chart1_categories.png")

plt.close()

# Chart 2
df['title'].head(10).value_counts().plot(kind='barh')
plt.title("Top Stories")
plt.savefig("outputs/chart2_top_stories.png")
plt.close()

# Chart 3
df.plot.scatter(x='score', y='comments')
plt.title("Score vs Comments")
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)
