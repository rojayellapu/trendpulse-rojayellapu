import requests
import pandas as pd
import time
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "https://hacker-news.firebaseio.com/v0"
headers = {"User-Agent": "TrendPulse/1.0"}

# ---------------- CATEGORIES ---------------- #
categories = {
    "technology": ["AI","software","tech","code","computer","data","cloud","API","GPU","LLM"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["NFL","NBA","FIFA","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","NASA","genome"],
    "entertainment": ["movie","film","music","Netflix","game","book","show","award","streaming"]
}

# normalize keywords
categories = {
    cat: [word.casefold() for word in words]
    for cat, words in categories.items()
}

# ---------------- FETCH IDS ---------------- #
try:
    res = requests.get(f"{base_url}/topstories.json", headers=headers, timeout=10)
    res.raise_for_status()
    ids = res.json()
except Exception as e:
    print("Error while getting IDs:", e)
    ids = []

# ---------------- FETCH STORIES (PARALLEL) ---------------- #
def fetch_story(story_id):
    try:
        r = requests.get(f"{base_url}/item/{story_id}.json", headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

stories = []

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(fetch_story, i) for i in ids[:300]]

    for future in as_completed(futures):
        result = future.result()
        if result:
            stories.append(result)

df = pd.DataFrame(stories)

# ---------------- PROCESS ---------------- #
results = []
seen_ids = set()  # avoid duplicates across categories

for cat, keywords in categories.items():
    count = 0

    for idx in range(len(df)):
        title = str(df.get("title", "").iloc[idx]) if "title" in df else ""
        title_lower = title.casefold()

        if any(f" {kw} " in f" {title_lower} " for kw in keywords):

            post_id = df.get("id", pd.Series([None])).iloc[idx]

            if post_id in seen_ids:
                continue

            if count < 25:
                results.append({
                    "post_id": post_id,
                    "title": title,
                    "category": cat,
                    "score": df.get("score", pd.Series([0])).iloc[idx] or 0,
                    "num_comments": df.get("descendants", pd.Series([0])).iloc[idx] or 0,
                    "author": df.get("by", pd.Series(["unknown"])).iloc[idx],
                    "url": df.get("url", pd.Series([""])).iloc[idx],
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                seen_ids.add(post_id)
                count += 1
            else:
                break

df_final = pd.DataFrame(results)

print(df_final.shape)
print(df_final.head())

# ---------------- SAVE ---------------- #
os.makedirs("data", exist_ok=True)

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as file:
    json.dump(results, file, indent=4, default=int)

# also save CSV (optional but useful)
df_final.to_csv(filename.replace(".json", ".csv"), index=False)

print(f"Collected {df_final.shape[0]} stories. Saved to {filename}")
