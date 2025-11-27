# Traffic Control and Urban Mobility via YOLOv7

Traffic in metropolitan cities, as we know, has become a part of the bustling culture. But, as traffic piles up at important junctions and such, they also result in more emissions from idle vehicles, and it is also noticeable that the traffic signals used follow a timer, which is constant and has the same countdown, even if there's minimal traffic compared to that of the others.

- This project aims to reduce such conflicts with the help of **vehicle classification** using **YOLOv7**.
- **Custom-labelled** datasets for accurate prediction and to reduce false positives.
- A **class-wise threshold** detection is also set, which is widely **customizable**.
- Along with it, a simple **GUI** is created, which provides simplistic control over the parameters present.
- Functions with both **live feeds** and **pre-recorded** traffic cam frames.
- **Multi-feed** access is a bit buggy, will be updated as soon as it's resolved.

# Instructions:

1. clone the following repository if you want to train with your custom data:
(note: this repo is optional, but a must-have for re-training and should be in a separate folder:)

                            cd dir/yolov7
   
                            git clone https://github.com/WongKinYiu/yolov7

2. then, on a separate location, clone this repo:
   
                            cd dir/folder

                            git clone https://github.com/rishi-naath/Traffic-Control-and-Urban-Mobility-via-YOLOv7/edit/main/README.md

3. as usual, now use the requirements file to download the necessities:

                           pip install -r requirements.txt

