import os
import json
import subprocess
from tqdm import tqdm

# Ensure yt-dlp is installed: pip install yt-dlp

# Directory to save videos
save_dir = 'videos'
os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

# Load JSON data
with open('data/mlb-youtube-segmented.json', 'r') as f:
    data = json.load(f)

# Loop through video entries
for video_id, entry in tqdm(data.items()):
    yturl = entry['url']
    ytid = yturl.split('=')[-1]
    start_time = entry['start']
    end_time = entry['end']
    output_path = os.path.join(save_dir, f"{ytid}_{int(start_time)}-{int(end_time)}.mkv")

    # Skip if video segment already exists
    if os.path.exists(output_path):
        print(f"Skipping {ytid}, already downloaded.")
        continue

    # Download specific section using yt-dlp
    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mkv",
        "--download-sections", f"*{start_time}-{end_time}",
        "-o", output_path,
        yturl
    ]

    print(f"Downloading {yturl} from {start_time} to {end_time} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Print errors if download fails
    if result.returncode != 0:
        print(f"Error downloading {ytid}: {result.stderr}")
    else:
        print(f"Downloaded {ytid} successfully.")
