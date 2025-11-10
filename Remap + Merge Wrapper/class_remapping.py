import os

#Define remapping for each dataset
remap_A = {"0": "1", "1": "2", "2": "3"}  # car, motorcycle, truck
remap_B = {"0": "0", "1": "1", "2": "2", "3": "3"}  # bus, car, motorcycle, truck

#Dataset paths
dataset_A = r"path\to\dataset_A"
dataset_B = r"path\to\dataset_B"
splits = ["train", "val"]

def remap_labels(base_path, remap_dict):
    for split in splits:
        label_dir = os.path.join(base_path, split, "labels")
        if not os.path.exists(label_dir):
            print(f"Skipping missing folder: {label_dir}")                            
            continue

        for filename in os.listdir(label_dir):
            if not filename.endswith(".txt"):
                continue

            file_path = os.path.join(label_dir, filename)                            
            with open(file_path, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                old_id = parts[0]
                new_id = remap_dict.get(old_id, old_id)
                new_line = " ".join([new_id] + parts[1:])
                new_lines.append(new_line)

            with open(file_path, "w") as f:
                f.write("\n".join(new_lines) + "\n")

            print(f"Updated: {file_path}")

#Run remapping
remap_labels(dataset_A, remap_A)
remap_labels(dataset_B, remap_B)

print("Completed.")
