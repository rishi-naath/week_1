import os
import shutil

#Source datasets
dataset_A = r"path\to\dataset_A"
dataset_B = r"path\to\dataset_B"

#Destination merged dataset
merged_dataset = r"directory\to\your\merged\dataset"
splits = ["train", "val"]

for split in splits:
    for subfolder in ["images", "labels"]:
        os.makedirs(os.path.join(merged_dataset, split, subfolder), exist_ok=True)

    for source in [dataset_A, dataset_B]:
        src_img_dir = os.path.join(source, split, "images") #Source image
        src_lbl_dir = os.path.join(source, split, "labels") #Source label
        dst_img_dir = os.path.join(merged_dataset, split, "images") #Dest. Image
        dst_lbl_dir = os.path.join(merged_dataset, split, "labels") #Dest. Label

        if not os.path.exists(src_img_dir):
            continue

        for file in os.listdir(src_img_dir):
            src_file = os.path.join(src_img_dir, file)
            dst_file = os.path.join(dst_img_dir, file)
            if os.path.exists(dst_file):
                name, ext = os.path.splitext(file)                                                   #To copy files from source to the destination w/o overwriting
                dst_file = os.path.join(dst_img_dir, f"{name}_{os.path.basename(source)}{ext}")           #The duplicate files will be renamed with (1), (2), etc...
            shutil.copy2(src_file, dst_file)

        for file in os.listdir(src_lbl_dir):
            src_file = os.path.join(src_lbl_dir, file)
            dst_file = os.path.join(dst_lbl_dir, file)
            if os.path.exists(dst_file):
                name, ext = os.path.splitext(file)                                                    #Similar function
                dst_file = os.path.join(dst_lbl_dir, f"{name}_{os.path.basename(source)}{ext}")
            shutil.copy2(src_file, dst_file)

print("Datasets merged into 'final'.")
