import os
import yaml
import json
import time
import logging
from collections import defaultdict

# === CONFIGURATION ===
yaml_path = r'path\to\your\config'
with open(r"directory\where\label\is\created", "r") as f:
    label_dir = f.read().strip()
save_dir = r'dir\to\your\save'
filename = "detected_results.txt"
LATEST_JSON = os.path.join(save_dir, "latest_counts.json")

class_thresholds = {
    "truck": 0.25,
    "bus": 0.25,
    "car": 0.25,
    "motorcycle": 0.25
}
filtered_classes = ["truck", "bus", "car", "motorcycle"]

# === LOAD CLASS NAMES ===
with open(yaml_path, 'r') as f:
    class_names_raw = yaml.safe_load(f)['names']
    class_names = [name.lower() for name in class_names_raw]

class_thresholds = {k.lower(): v for k, v in class_thresholds.items()}
filtered_classes = [cls.lower() for cls in filtered_classes]

os.makedirs(save_dir, exist_ok=True)
log_path = os.path.join(save_dir, filename)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    filemode='w'
)

def process_label_file(file_path):
    local_counts = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 6:
                class_id = int(parts[0])
                conf = float(parts[-1])
            elif len(parts) == 5:
                class_id = int(parts[0])
                conf = 0.5
            else:
                continue
            if class_id >= len(class_names):
                continue
            class_name = class_names[class_id]
            if class_name in class_thresholds and conf >= class_thresholds[class_name]:
                local_counts[class_name] += 1
    return local_counts

def write_snapshot(file_name, local_counts):                  #creates a dedicated .txt file to mark the vehicles counted per frame
    snapshot = {
        "ts": time.time(),
        "frame": file_name,
        "counts": {k: int(v) for k, v in local_counts.items()}
    }
    with open(LATEST_JSON, "w", encoding="utf-8") as f:
        json.dump(snapshot, f)
        f.flush()
        os.fsync(f.fileno())    

def main_loop():
    print("[INFO] class_filter.py started. Computing rolling average over first 40 label files...")
    print(f"[DEBUG] Watching label_dir: {label_dir}")
    try:
        files = sorted(f for f in os.listdir(label_dir) if f.endswith(".txt"))[:40]
    except FileNotFoundError:
        files = []

    rolling_sum = defaultdict(int)
    count_frames = 0

    for f in files:
        path = os.path.join(label_dir, f)
        try:
            counts = process_label_file(path)
            for cls in filtered_classes:
                rolling_sum[cls] += counts.get(cls, 0)
            count_frames += 1
        except Exception as e:
            print(f"[ERROR] Failed to process {f}: {e}")

    if count_frames > 0:
        averaged_counts = {cls: int(rolling_sum[cls] / count_frames) for cls in filtered_classes}
        write_snapshot(f"rolling_avg_{count_frames}_frames", averaged_counts)
        print(f"[INFO] Rolling average over {count_frames} frames: {averaged_counts}")
    else:
        print("[INFO] No valid detections found.")


if __name__ == "__main__":
    while True:
        main_loop()
        time.sleep(1.0)

