import shutil
import json
from pathlib import Path
from datetime import datetime

def sync_assets():
    # Create directories if they don't exist
    Path("docs/assets/img").mkdir(parents=True, exist_ok=True)
    Path("docs/assets/data").mkdir(parents=True, exist_ok=True)

    # Copy image files from output/ to docs/assets/img/
    for img_file in Path("output").glob("*.png"):
        shutil.copy(img_file, "docs/assets/img/")

    # Copy and update articles.json
    with open("data/articles.json", "r") as f:
        articles_data = {
            "articles": json.load(f),
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "source": "data/articles.json"
            }
        }
    
    with open("docs/assets/data/articles.json", "w") as f:
        json.dump(articles_data, f, indent=2)

if __name__ == "__main__":
    sync_assets()
    print("Dashboard assets synchronized successfully")
