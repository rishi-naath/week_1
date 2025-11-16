# orchestrator_gui.py (patched)
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import time
import signal
import sys
import glob
import datetime
import yaml

# === PATHS TO SCRIPTS ===
DETECT_SCRIPT = r"yolov7/detect/script"
LOGGING_SCRIPT = r"class_filter/directory"
SIGNAL_SCRIPT = r"virtual/signal/script"
WEIGHTS_PATH = r"directory/to/best/weights"

# === DETECTION OUTPUT ===
DETECT_PROJECT = r"path/of/detect/folder"
DETECT_RUN_NAME = f"gui_run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
LABEL_DIR = os.path.join(DETECT_PROJECT, DETECT_RUN_NAME, "labels")

# === Runtime files ===
LABEL_PATH_FILE = r"dir/to/write/label"
VIDEO_PATH_FILE = r"dir/to/video/path"
LATEST_JSON = r"in the form of/detected_results/detected.json"

processes = []
proc_lock = threading.Lock()

def purge_old_outputs():
    # Delete old label files if folder exists
    if os.path.isdir(LABEL_DIR):
        for f in os.listdir(LABEL_DIR):
            if f.endswith(".txt"):
                try:
                    os.remove(os.path.join(LABEL_DIR, f))
                except Exception:
                    pass

    # Delete stale JSON
    json_path = os.path.join(".....\\Class-wise Detection\\detected_results", "latest_counts.json")
    try:
        os.remove(json_path)
    except Exception:
        pass

# GUI status logging
def gui_log(text_widget, msg):
    text_widget.configure(state='normal')
    text_widget.insert(tk.END, msg + "\n")
    text_widget.see(tk.END)
    text_widget.configure(state='disabled')

def run_detection(source, conf_thres, status_widget):
    # build explicit YOLO detect command that forces label output in known folder
    cmd = [
    sys.executable, DETECT_SCRIPT,
    "--source", str(source),
    "--weights", r"best/weights/path",
    "--save-txt",
    "--save-conf",
    "--project", DETECT_PROJECT,
    "--name", DETECT_RUN_NAME,
    "--exist-ok",
    "--conf", str(conf_thres)
   ]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.path.dirname(DETECT_SCRIPT))
    except Exception as e:
        gui_log(status_widget, f"[DETECT] start failed: {e}")
        return
    with proc_lock:
        processes.append(p)
    gui_log(status_widget, f"[DETECT] started pid={p.pid}")
    gui_log(status_widget, f"[DETECT] Running command: {' '.join(cmd)}")

    # drain stdout/stderr to GUI
    def drain(pipe, prefix):
        for line in iter(pipe.readline, ''):
            gui_log(status_widget, f"{prefix}: {line.rstrip()}")
        pipe.close()
    threading.Thread(target=drain, args=(p.stdout, "DETECT_OUT"), daemon=True).start()
    threading.Thread(target=drain, args=(p.stderr, "DETECT_ERR"), daemon=True).start()

def wait_for_labels(timeout=15, status_widget=None):
    deadline = time.time() + timeout
    while time.time() < deadline:
        txts = glob.glob(os.path.join(LABEL_DIR, "*.txt"))
        if txts:
            if status_widget:
                gui_log(status_widget, f"[SYNC] found {len(txts)} label files, continuing")
            return True
        time.sleep(0.3)
    if status_widget:
        gui_log(status_widget, "[SYNC] no label files found within timeout")
    return False

def run_logging(status_widget):
    try:
        p = subprocess.Popen([sys.executable, LOGGING_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.path.dirname(LOGGING_SCRIPT))
    except Exception as e:
        gui_log(status_widget, f"[LOG] start failed: {e}")
        return
    with proc_lock:
        processes.append(p)
    gui_log(status_widget, f"[LOG] started pid={p.pid}")
    def drain(pipe, prefix):
        for line in iter(pipe.readline, ''):
            gui_log(status_widget, f"{prefix}: {line.rstrip()}")
        pipe.close()
    gui_log(status_widget, "[LOG] class_filter.py launched")
    threading.Thread(target=drain, args=(p.stdout, "LOG_OUT"), daemon=True).start()
    threading.Thread(target=drain, args=(p.stderr, "LOG_ERR"), daemon=True).start()
    

def run_signal_overlay(status_widget):
    try:
        p = subprocess.Popen([sys.executable, SIGNAL_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=os.path.dirname(SIGNAL_SCRIPT))
    except Exception as e:
        gui_log(status_widget, f"[SIGNAL] start failed: {e}")
        return
    with proc_lock:
        processes.append(p)
    gui_log(status_widget, f"[SIGNAL] started pid={p.pid}")
    def drain(pipe, prefix):
        for line in iter(pipe.readline, ''):
            gui_log(status_widget, f"{prefix}: {line.rstrip()}")
        pipe.close()
    threading.Thread(target=drain, args=(p.stdout, "SIGNAL_OUT"), daemon=True).start()
    threading.Thread(target=drain, args=(p.stderr, "SIGNAL_ERR"), daemon=True).start()

def stop_pipeline(status_widget):
    with proc_lock:
        for p in processes:
            try:
                gui_log(status_widget, f"[STOP] terminating pid={p.pid}")
                p.terminate()
            except Exception:
                pass
        # give them a second, then kill
        time.sleep(1.0)
        for p in processes:
            if p.poll() is None:
                try:
                    p.kill()
                except Exception:
                    pass
        processes.clear()
    gui_log(status_widget, "[STOP] all modules terminated")


def launch_from_gui(source, conf, status_widget):
    stop_pipeline(status_widget)
    purge_old_outputs()

    gui_log(status_widget, f"[LAUNCH] Selected source: {source}")
    gui_log(status_widget, f"[LAUNCH] Confidence: {conf}")

    # Save label_dir to temp file for class_filter.py
    try:
        with open(r"N:\College\Anotha_Internship\Class-wise Detection\label_path.txt", "w") as f:
            f.write(LABEL_DIR)
        gui_log(status_widget, f"[LAUNCH] label_path.txt written: {LABEL_DIR}")
    except Exception as e:
        gui_log(status_widget, f"[ERROR] Failed to write label_path.txt: {e}")

    # Save selected video path for dig_tr_sgn.py
    try:
        with open(r"N:\College\Anotha_Internship\Class-wise Detection\video_path.txt", "w") as f:
            f.write(str(source))
        gui_log(status_widget, f"[LAUNCH] video_path.txt written: {source}")
    except Exception as e:
        gui_log(status_widget, f"[ERROR] Failed to write video_path.txt: {e}")

    threading.Thread(target=run_detection, args=(source, conf, status_widget), daemon=True).start()
    threading.Thread(target=sync_and_start_rest, args=(status_widget,), daemon=True).start()

def sync_and_start_rest(status_widget):
    # wait a bit for detection to spin up and create labels
    found = wait_for_labels(timeout=20, status_widget=status_widget)
    if not found:
        gui_log(status_widget, "[SYNC] warning: no labels found; starting logging/signal anyway")
    run_logging(status_widget)
    run_signal_overlay(status_widget)

# === GUI ===
def build_gui():
    root = tk.Tk()
    root.title("Traffic AI Control Panel")
    root.geometry("700x520")
    # Inputs frame
    top = tk.Frame(root)
    top.pack(pady=8, fill=tk.X)

    tk.Label(top, text="Source (file path or camera index):", font=("Arial", 10)).pack(anchor='w')
    source_entry = tk.Entry(top, width=60)
    source_entry.insert(0, "0")  # default to webcam 0
    source_entry.pack(anchor='w', padx=6)

    def browse_file():
        p = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.avi *.mov"), ("All", "*.*")])
        if p:
            source_entry.delete(0, tk.END)
            source_entry.insert(0, p)

    tk.Button(top, text="Browse video file", command=browse_file).pack(anchor='w', padx=6, pady=4)

    # config frame
    cfg = tk.LabelFrame(root, text="Config", padx=8, pady=8)
    cfg.pack(fill=tk.X, padx=8, pady=6)

    tk.Label(cfg, text="Confidence (float)").grid(row=0, column=0, sticky='w')
    conf_entry = tk.Entry(cfg, width=8)
    conf_entry.insert(0, "0.25")
    conf_entry.grid(row=0, column=1, sticky='w')

    tk.Label(cfg, text="Car threshold").grid(row=1, column=0, sticky='w')
    car_entry = tk.Entry(cfg, width=6); car_entry.insert(0, "10"); car_entry.grid(row=1, column=1, sticky='w')
    tk.Label(cfg, text="Bus threshold").grid(row=1, column=2, sticky='w')
    bus_entry = tk.Entry(cfg, width=6); bus_entry.insert(0, "1"); bus_entry.grid(row=1, column=3, sticky='w')
    tk.Label(cfg, text="Truck threshold").grid(row=2, column=0, sticky='w')
    truck_entry = tk.Entry(cfg, width=6); truck_entry.insert(0, "2"); truck_entry.grid(row=2, column=1, sticky='w')
    tk.Label(cfg, text="Motorcycle threshold").grid(row=2, column=2, sticky='w')
    moto_entry = tk.Entry(cfg, width=6); moto_entry.insert(0, "3"); moto_entry.grid(row=2, column=3, sticky='w')

    # status / log area
    status_frame = tk.LabelFrame(root, text="Status / Logs", padx=6, pady=6)
    status_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    status_txt = scrolledtext.ScrolledText(status_frame, state='disabled', height=12)
    status_txt.pack(fill=tk.BOTH, expand=True)

    # control buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)
    def on_launch():
        src = source_entry.get().strip()
        if src == "":
            messagebox.showerror("Error", "Please enter a source (0 for webcam or video file path).")
            return
        # convert camera indices to int
        try:
            s = int(src)
        except Exception:
            s = src
        try:
            conf = float(conf_entry.get().strip())
        except Exception:
            messagebox.showerror("Error", "Invalid confidence value")
            return
        launch_from_gui(s, conf, status_txt)

    tk.Button(btn_frame, text="🚀 Launch Pipeline", bg="green", fg="white", width=18, command=on_launch).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="🛑 Stop Pipeline", bg="red", fg="white", width=18, command=lambda: stop_pipeline(status_txt)).grid(row=0, column=1, padx=8)

    root.mainloop()

if __name__ == "__main__":

    build_gui()
