# Traffic Control and Urban Mobility via YOLOv7

Traffic in metropolitan cities, as we know, has become a part of the bustling culture. But, as traffic piles up at important junctions and such, they also result in more emissions from idle vehicles, and it is also noticeable that the traffic signals used follow a timer, which is constant and has the same countdown, even if there's minimal traffic compared to that of the others.

- This project aims to reduce such conflicts with the help of **vehicle classification** using **YOLOv7**.
- **Custom-labelled** datasets for accurate prediction and to reduce false positives.
- Detection is done over a specified **ROI (Region of Interest)** to reduce load and improve effectiveness.
- A **class-wise threshold** detection is also set, which is widely **customizable**.
- Along with it, a simple **GUI** is created, which provides simplistic control over the parameters present.
- Functions with both **live feeds** and **pre-recorded** traffic cam frames.
- **Multi-feed** access is a bit buggy, will be updated as soon as it's resolved.

<img width="600" height="700" alt="Screenshot 2025-11-27 140436" src="https://github.com/user-attachments/assets/b113b13c-9dc0-4598-bce5-7c3eb80be67f" />


<img width="1919" height="1079" alt="Screenshot 2025-11-27 180634" src="https://github.com/user-attachments/assets/8502b346-d966-44a2-bbbb-e3cb0e56f4ee" />

# Instructions:

1. Clone the following repository if you want to train with your custom data:
(note: this repo is optional, but a must-have for re-training and should be in a separate folder:)

                            cd dir/yolov7
   
                            git clone https://github.com/WongKinYiu/yolov7

2. Then, on a separate location, clone this repo:
   
                            cd dir/folder

                            git clone https://github.com/rishi-naath/Traffic-Control-and-Urban-Mobility-via-YOLOv7

3. As usual, now use the requirements file to download the necessities:

                           pip install -r requirements.txt
(**FYI:** I've used **YOLOv7**, so the dependencies are a bit old; nonetheless, you should be good if you used them in venv)

# Precautions:

- Make sure to **double-check** the **paths** specified on all the modules, if you're running locally, specify hard-coded paths for the following:
  - In **class_filter.py,** from **line 9-13:**
    - yaml_path = r'data.yaml'
    - with open(r'Class_Filter\label_path.txt', "r")
    - save_dir = r'Class_Filter\detected_results'

  - In **dig_sig_tr.py, line 9 and 10:**
    - LATEST_JSON = r'Class_Filter\detected_results\latest_counts.json'
    - video_path_file = r'Class_Filter\video_path.txt')
   
  - In **traffic_predict_final.py, line 15 to 28:**
    - DETECT_SCRIPT = r'detect\detect.py'
    - LOGGING_SCRIPT = r'Class_Filter\class_filter.py'
    - SIGNAL_SCRIPT = r'Digital_Traffic_Signal\dig_tr_sgn.py'
    - WEIGHTS_PATH = r'Weights\best.pt'
    - DETECT_PROJECT = r'yolov7\runs\detect'
    - LABEL_PATH_FILE = r'Class_Filter\label_path.txt'
    - VIDEO_PATH_FILE = r'Class_Filter\video_path.txt'
    - LATEST_JSON = r'Class_Filter\detected_results\latest_count.json'
    - **line 62:** "weights", r'Weights\best.pt'
    - **line 164:** with open(r'Class_Filter\label_path.txt', "w") as f:
    - **line 172:** with open(r'Class_Filter\video_path.txt', "w") as f:
