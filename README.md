# Traffic Control and Urban Mobility via YOLOv7

Traffic in metropolitan cities, as we know, has become a part of the bustling culture. But, as traffic piles up at important junctions and such, they also result in more emissions from idle vehicles, and it is also noticeable that the traffic signals used follow a timer, which is constant and has the same countdown, even if there's minimal traffic compared to that of the others.

- This project aims to reduce such conflicts with the help of ***vehicle classification*** using **YOLOv7**.
- ***Custom-labelled*** datasets for accurate prediction and to reduce false positives.
- Detection is done over a specified ***ROI (Region of Interest)*** to reduce load and improve effectiveness.
- A ***class-wise threshold*** detection is also set, which is widely **customizable**.
- Along with it, a simple ***GUI*** is created, which provides simplistic control over the parameters present.
- Functions with both ***live feeds*** and **pre-recorded** traffic cam frames (0 for live feed, and directory for pre-recorded).
- ***Multi-feed*** access is a bit buggy, will be updated as soon as it's resolved.

<img width="600" height="700" alt="Screenshot 2025-11-27 140436" src="https://github.com/user-attachments/assets/b113b13c-9dc0-4598-bce5-7c3eb80be67f" />


<img width="1919" height="1079" alt="Screenshot 2025-11-27 180634" src="https://github.com/user-attachments/assets/8502b346-d966-44a2-bbbb-e3cb0e56f4ee" />


# Instructions:

1. Clone the following repository if you want to train with your custom data:
(*note: this repo is optional, but a must-have for re-training and should be in a separate folder:*)

                            cd dir/yolov7
   
                            git clone https://github.com/WongKinYiu/yolov7

2. Then, on a separate location, clone this repo:
   
                            cd dir/folder

                            git clone https://github.com/rishi-naath/Traffic-Control-and-Urban-Mobility-via-YOLOv7

3. As usual, now use the requirements file to download the necessities:

                           pip install -r requirements.txt
(****FYI:*** I've used **YOLOv7**, so the dependencies are a bit old; nonetheless, you should be good if you used them in venv*)

# Precautions:

- Make sure to **double-check** the **paths** specified on all the modules. If you're running locally, specify hard-coded paths for the following:
  - In **class_filter.py,** from ***line 9-13:***
  
         yaml_path = r'data.yaml'
         with open(r'Class_Filter\label_path.txt', "r")
         save_dir = r'Class_Filter\detected_results'

  - In **dig_sig_tr.py,** ***line 9 and 10:***

         LATEST_JSON = r'Class_Filter\detected_results\latest_counts.json'
         video_path_file = r'Class_Filter\video_path.txt')
   
  - In **traffic_predict_final.py,**
 
    ***line 15 to 28:***

         DETECT_SCRIPT = r'detect\detect.py'
         LOGGING_SCRIPT = r'Class_Filter\class_filter.py'
         SIGNAL_SCRIPT = r'Digital_Traffic_Signal\dig_tr_sgn.py'
         WEIGHTS_PATH = r'Weights\best.pt'
         DETECT_PROJECT = r'yolov7\runs\detect'
         LABEL_PATH_FILE = r'Class_Filter\label_path.txt'
         VIDEO_PATH_FILE = r'Class_Filter\video_path.txt'
         LATEST_JSON = r'Class_Filter\detected_results\latest_count.json'
     ***line 62:***

         "weights", r'Weights\best.pt'
     ***line 164:***

         with open(r'Class_Filter\label_path.txt', "w") as f:
     ***line 172:***

         with open(r'Class_Filter\video_path.txt', "w") as f:

# Metrics:

# *General ROI specified: (hand-drawn for reference):*

<img width="1919" height="1079" alt="ROI" src="https://github.com/user-attachments/assets/ee31ae65-13f6-4fec-b5d2-542091b08eaf" />


# *Metrics observed via TensorboardRT:*
<img width="1151" height="585" alt="metrics_precision" src="https://github.com/user-attachments/assets/3cc5c935-fe8f-47b8-9c98-3a25408df23d" />

<img width="1159" height="593" alt="train_obj_loss" src="https://github.com/user-attachments/assets/ac0753e4-00a2-462f-8f47-c9b1f55fc359" />

<img width="1155" height="584" alt="val_obj_loss" src="https://github.com/user-attachments/assets/341aec9e-fd65-4525-bea0-8eb4de9339ae" />

# *Metrics generated after training completion:*
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/52681cf2-79b5-431e-98ad-5a03660c1bdf" />

# *Train and Test Observations:*

# *Train:*

![train_batch0](https://github.com/user-attachments/assets/35a12566-212a-4228-b04b-fbe67f6ce724)


![train_batch1](https://github.com/user-attachments/assets/22c371c8-ce66-42f4-95e2-dc6e2b1f0fec)


# *Test:*


![test_batch1_labels](https://github.com/user-attachments/assets/69ab38f2-76dc-4f8e-beba-bc96215b09ce)


![test_batch1_pred](https://github.com/user-attachments/assets/5b480b25-c97a-43b7-aeb0-b744c5407240)


# Acknowledgements:
  
  - https://github.com/WongKinYiu/yolov7
  - https://www.kaggle.com/datasets/brsdincer/vehicle-detection-image-set/data
  - https://www.kaggle.com/datasets/farzadnekouei/top-view-vehicle-detection-image-dataset
  - https://www.kaggle.com/datasets/saumyapatel/traffic-vehicles-object-detection?select=Traffic+Dataset
  - https://github.com/tensorflow/tensorboard

# Extras:

  - Specifics of each module are specified in both the ***readme*** and inside them.
  - If in need of merging multiple datasets and syncing/relabelling the labels, make use of ***Remap+Merge Wrapper*** modules that might be of help.
  - Notebook versions are also added for straightforward explanation with fewer tech terms.

# *Do ping or create a pull request if you're able to optimize and improve the functionality.*

Contact: rishinaath33@gmail.com
