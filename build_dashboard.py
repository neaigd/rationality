import shutil
import json
import zipfile
from pathlib import Path
from datetime import datetime

def sync_assets():
    # Create directories if they don't exist
    Path("docs/assets/img").mkdir(parents=True, exist_ok=True)
    Path("docs/assets/data").mkdir(parents=True, exist_ok=True)
    
    # Extract dashboard template
    template_dir = Path("dashboard_template/extracted")
    template_dir.mkdir(exist_ok=True)
    
    with zipfile.ZipFile("dashboard_template/startbootstrap-sb-admin-2-gh-pages.zip", 'r') as zip_ref:
        zip_ref.extractall(template_dir)
    
    # Copy dashboard files
    source_dir = template_dir / "startbootstrap-sb-admin-2-gh-pages"
    shutil.copy(source_dir / "index.html", "docs/")
    for file in source_dir.glob('*'):
        if file.is_file() and file.suffix in ['.css', '.js']:
            shutil.copy(file, "docs/")

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
    try:
        sync_assets()
        if not Path("docs/index.html").exists():
            raise RuntimeError("Critical error: index.html was not generated in docs/")
        print("Dashboard assets synchronized successfully")
    except Exception as e:
        print(f"Error during dashboard build: {str(e)}")
        raise
