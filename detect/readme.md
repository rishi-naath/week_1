A **modified** version of **WongKinYiu's** base detect file

When executed as a standalone:

- Shows the directory in which the labels detected are being stored ([DEBUG]:).

- Now provides dynamic unit-selection (i.e, CPU or GPU) based on user selection (default = cpu)

# cmd to run as a standalone:

    python detect.py --weights "weights/best.pt" 
    --source "Test_Footage/traffic_1.mp4" 
    --conf 0.25                                        
    --img-size 640 
    --save-txt 
    --view-img

