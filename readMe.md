# AI Human Activity Recognition for On-Board BAS Experiments

## 🚀 Overview

This project is an **AI-based Human Activity Recognition (HAR) system** designed for autonomous experiment monitoring in space environments such as **BAS (Bharatiya Antariksh Station)** and future lunar missions.

The system processes video locally from a camera and recognizes objects, human pose, interactions, and experiment steps without requiring continuous communication with ground control.

The main objective is to verify that an astronaut performs a predefined experiment in the correct sequence.

### Core capabilities

* 🎥 Live camera processing
* 🧠 AI-based object detection
* 🧍 Human pose estimation
* 🔄 Experiment step/sequence validation
* 🗣️ Offline Text-to-Speech (TTS) alerts
* ⚠️ Step missed detection
* ⚠️ Out-of-sequence detection
* 📋 Timestamped experiment logging
* 💾 Local video recording
* 🖥️ GUI-based monitoring
* 🌐 Optional IP video streaming
* 🔌 Offline operation after initial setup
* 🧪 Configurable experiments

---

# 🏗️ System Architecture

```text
Camera
   │
   ▼
Video Capture
   │
   ├──────────────► YOLOv8 Pose
   │                    │
   │                    ▼
   │              Human Wrist/Pose
   │
   └──────────────► RF-DETR Object Detection
                        │
                        ▼
                 Object Detection
                        │
                        ▼
              Experiment Conditions
                        │
                        ▼
                 Step Validation
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
        GUI            TTS          Logger
          │             │             │
          ▼             ▼             ▼
      Monitoring     Voice Alert   JSONL Log
                                      │
                                      ▼
                                Local Storage
```

---

# 📁 Project Structure

The recommended project structure is:

```text
BAS_based_HAR_system-main/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── venv312/
│
├── src/
│   ├── __init__.py
│   ├── detector.py
│   ├── conditions.py
│   ├── tracker.py
│   ├── dag.py
│   ├── tts_alerts.py
│   ├── logger.py
│   ├── camera.py
│   └── gui.py
│
├── models/
│   └── yolov8n-pose.pt
│
└── data/
    ├── experiments/
    │   └── experiments.json
    │
    ├── logs/
    │
    └── videos/
```

### Important files

| File / Folder                       | Purpose                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `main.py`                           | Main program / application entry point                 |
| `config.py`                         | Global configuration and experiment settings           |
| `requirements.txt`                  | Python dependencies                                    |
| `src/detector.py`                   | YOLOv8 pose + RF-DETR object detection                 |
| `src/conditions.py`                 | Determines whether experiment conditions are satisfied |
| `src/tracker.py`                    | Confirms detections over multiple frames               |
| `src/dag.py`                        | Handles experiment sequence/order                      |
| `src/tts_alerts.py`                 | Offline voice alerts                                   |
| `src/logger.py`                     | Experiment event logging                               |
| `src/camera.py`                     | Camera capture, recording and optional streaming       |
| `src/gui.py`                        | Graphical monitoring interface                         |
| `data/experiments/experiments.json` | Experiment definitions                                 |
| `data/logs/`                        | Generated experiment logs                              |
| `data/videos/`                      | Recorded experiment videos                             |
| `models/`                           | Local AI model files                                   |

The original project design uses separate detector, tracker, DAG, TTS, logger, camera and GUI modules for this purpose.

---

# 💻 Requirements

## Hardware

Recommended:

* Windows laptop/PC
* Webcam or laptop camera
* Minimum 8 GB RAM
* Recommended 16 GB RAM
* CPU capable of running PyTorch
* GPU optional but recommended for faster inference

For the current development setup, the **laptop's built-in camera** can be used.

---

# 🐍 Python Environment

Python should be installed before starting the project.

Check Python:

```powershell
python --version
```

Example:

```text
Python 3.12.x
```

---

# 🔧 1. Create Virtual Environment

Open the project in VS Code.

Open:

```text
Terminal → New Terminal
```

Navigate to the project directory:

```powershell
cd "D:\New folder\BAS_based_HAR_system-main"
```

Create the virtual environment:

```powershell
python -m venv venv312
```

Activate it:

```powershell
venv312\Scripts\activate
```

You should now see:

```text
(venv312)
```

at the beginning of your terminal.

For example:

```text
(venv312) PS D:\New folder\BAS_based_HAR_system-main>
```

---

# 📦 2. Install Dependencies

With the virtual environment activated:

```powershell
pip install -r requirements.txt
```

If some packages are missing, install the main dependencies manually:

```powershell
pip install ultralytics opencv-python numpy pyttsx3 inference pillow
```

The project requires packages for:

* YOLOv8
* OpenCV
* NumPy
* RF-DETR / Roboflow inference
* Text-to-Speech
* Image processing

---

# 🤖 3. AI Models

The project uses two main AI components.

## YOLOv8 Pose

YOLOv8 Pose is used for human pose estimation.

It provides body keypoints such as:

```text
Left Wrist
Right Wrist
```

These points are used to determine interactions between the astronaut's hands and detected objects.

The project originally used YOLOv8 models that could be downloaded automatically on first execution.

---

## RF-DETR Object Detection

The custom experiment objects are detected using a Roboflow-trained model.

Example classes:

```text
container
lid
spoon
```

Your Roboflow model must be trained with correctly labelled objects.

For example:

```text
container → container
lid       → lid
spoon     → spoon
```

The model ID configured in `config.py` must match the current deployed/trained model version.

Example:

```python
ROBOFLOW_MODEL_ID = "bas-dgyu0/2"
```

If you train a new version, update this value accordingly.

---

# 🔑 4. Configure Roboflow

Open:

```text
config.py
```

Find:

```python
ROBOFLOW_API_KEY = "paste_your_private_api_key_here"
```

Replace it with your Roboflow private API key.

Example:

```python
ROBOFLOW_API_KEY = "YOUR_PRIVATE_API_KEY"
```

Then set the model ID:

```python
ROBOFLOW_MODEL_ID = "bas-dgyu0/2"
```

Make sure the model version corresponds to the model currently deployed in Roboflow.

---

# ⚠️ IMPORTANT: Never Upload Your API Key

Do **not** commit your private API key to GitHub.

Instead of:

```python
ROBOFLOW_API_KEY = "abc123..."
```

use an environment variable for a public GitHub repository.

For example:

```python
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
```

Then configure the key locally.

Also add your secrets to `.gitignore`.

---

# 📷 5. Camera Configuration

The current system can use your laptop camera.

In `config.py`:

```python
CAMERA_INDEX = 0
```

Usually:

```text
0 = built-in/default webcam
1 = second camera
2 = third camera
```

For a normal laptop webcam, use:

```python
CAMERA_INDEX = 0
```

---

# 🌐 6. IP Streaming

If the entire system is running on the same laptop, IP streaming is **not required**.

Set:

```python
STREAM_ENABLED = False
```

This is the recommended configuration for the current laptop-camera setup.

The system will still:

* show the live camera in the GUI
* process the camera
* record video locally
* run object detection
* run pose detection
* generate voice alerts
* generate logs

The previous project configuration also explicitly supports disabling streaming when everything is running on one machine.

---

# 📡 Optional IP Streaming

If a second computer needs to receive the video, enable:

```python
STREAM_ENABLED = True
STREAM_IP = "192.168.1.100"
STREAM_PORT = 5000
```

The receiving computer must be listening on the configured port.

This is optional and is **not necessary for the laptop-only demonstration**.

---

# 🧪 7. Configure the Experiment

Experiment logic is configurable.

The current example uses:

```text
Pick Up Container
Open Container
Use Spoon to Extract
Place Contents in Rack
Close Container
```

The sequence can be represented using:

```python
EXPERIMENT_STEPS = [
    "Pick Up Container",
    "Open Container",
    "Use Spoon to Extract",
    "Place Contents in Rack",
    "Close Container",
]
```

The project also defines detection conditions for each step.

Example:

```python
STEP_CONDITIONS = [
    {
        "objects": ["container"],
        "interaction": "motion_pickup"
    },

    {
        "objects": ["lid", "container"],
        "interaction": "separation"
    },

    {
        "objects": ["spoon", "container"],
        "interaction": "enter_exit"
    }
]
```

---

# 🔄 Experiment Sequence

The sequence is controlled using the DAG.

Example:

```python
DAG = {
    0: [1],
    1: [2],
    2: [3],
    3: [4]
}
```

This means:

```text
Step 0
  ↓
Step 1
  ↓
Step 2
  ↓
Step 3
  ↓
Step 4
```

The system can therefore determine whether an experiment step happens in the expected order.

---

# 🧠 Step Detection

The current condition system supports interactions such as:

### 1. Motion Pickup

The system checks:

```text
Hand near object
+
Object moves
```

Example:

```text
Pick up container
```

---

### 2. Separation

The system checks whether two objects move sufficiently far apart.

Example:

```text
Container
     ↓
Lid removed
```

---

### 3. Enter / Exit

The system first detects:

```text
Spoon inside container
```

and then:

```text
Spoon outside container
```

The complete inside → outside movement can be used to confirm the action.

---

### 4. Hand/Object Interaction

The pose detector provides wrist positions.

The system can calculate the distance between:

```text
Wrist
   ↓
Object
```

This helps determine whether an astronaut is interacting with an object.

---

# 🗣️ Offline Text-to-Speech

The project uses:

```text
pyttsx3
```

for local voice alerts.

No cloud TTS service is required.

Examples of alerts:

```text
Step done
```

```text
Next step: Open Container
```

```text
Alert: Step missed
```

```text
Alert: Out of sequence
```

```text
All steps complete. Experiment finished.
```

The TTS system was designed to run using the computer's local speech engine.

---

# 🔊 Test TTS Separately

If the system does not speak, test the Windows TTS engine directly:

```powershell
python -c "import pyttsx3; e=pyttsx3.init(); e.say('Test voice alert'); e.runAndWait()"
```

If you hear:

```text
Test voice alert
```

then the TTS engine is working.

---

# ▶️ 8. Start the Project

Every time you open VS Code again:

### Activate the virtual environment

```powershell
venv312\Scripts\activate
```

You should see:

```text
(venv312)
```

Then run:

```powershell
python main.py
```

This is the current main command for the newer project setup.

---

# 🚀 Complete Start Sequence

For a fresh terminal, use:

```powershell
cd "D:\New folder\BAS_based_HAR_system-main"
```

Then:

```powershell
venv312\Scripts\activate
```

Then:

```powershell
python main.py
```

---

# 🛑 9. Stop the Program

If the camera window is running:

```text
Q
```

can be used if the application supports the quit key.

The safest method from the VS Code terminal is:

```text
Ctrl + C
```

This stops the Python program.

---

# 📊 10. Output Files

After running an experiment, generated data is stored locally.

## Logs

```text
data/logs/
```

The system records events such as:

```text
experiment_start
step_confirmed
step_skipped
out_of_order
experiment_complete
experiment_end
```

The logs contain timestamps and experiment information.

---

## Videos

Recorded videos are stored in:

```text
data/videos/
```

This allows the experiment to be reviewed later.

---

# 🔌 11. Offline Operation

The system is designed for offline runtime operation.

## Internet is required initially for:

### Package installation

```powershell
pip install -r requirements.txt
```

### Initial model download

The required AI model files may need to be downloaded during the first setup.

### Model training

If the Roboflow dataset needs to be trained or retrained, internet is required during that training/deployment process.

---

# ✅ After Setup

Once the required packages and models are available locally, the actual experiment processing can run without continuous internet access.

The following components operate locally:

```text
Camera
   ↓
AI inference
   ↓
Pose detection
   ↓
Object detection
   ↓
Step validation
   ↓
TTS
   ↓
GUI
   ↓
Logging
   ↓
Video recording
```

The original project design specifically targeted standalone local processing because raw video does not need to be continuously transmitted to ground control.

---

# 🧪 12. Testing the Object Detector

Before testing the complete experiment, test the object detector separately.

The detector should correctly identify:

```text
container
lid
spoon
```

Do not move to experiment-step validation until the object detector reliably identifies these classes.

This is especially important because the experiment logic depends on the object detector's output.

---

# 🎯 Roboflow Dataset Requirements

Your training dataset should contain correctly labelled examples.

For example:

| Object    | Correct Label |
| --------- | ------------- |
| Container | `container`   |
| Lid       | `lid`         |
| Spoon     | `spoon`       |

Check several annotated images manually.

If every object is labelled:

```text
lid
```

the trained model may classify everything as `lid`.

The labels must be corrected before retraining.

---

# ⚡ 13. Performance / Lag

AI inference can be computationally expensive, particularly when running object detection and pose estimation simultaneously on a laptop CPU.

If the video becomes slow:

### Possible causes

* CPU-only inference
* High camera resolution
* Running pose detection every frame
* Running RF-DETR on every frame
* Large model
* High input resolution

### Possible optimization

Process detection every few frames while keeping the GUI updated continuously.

Example concept:

```python
if frame_n % 3 == 0:
    result = detector.detect(frame)
```

This reduces the number of expensive AI inference calls.

The earlier development testing also identified frame skipping as a practical approach for improving live-video responsiveness.

---

# 🐛 14. Troubleshooting

## `ModuleNotFoundError: No module named 'src'`

Make sure the project contains:

```text
src/
    __init__.py
    detector.py
```

and that `src` is located beside:

```text
main.py
```

Correct:

```text
project/
├── main.py
└── src/
    ├── __init__.py
    └── detector.py
```

---

## `ModuleNotFoundError: No module named 'ultralytics'`

Activate the virtual environment:

```powershell
venv312\Scripts\activate
```

Then install:

```powershell
pip install ultralytics
```

---

## Camera does not open

Check:

```python
CAMERA_INDEX = 0
```

Also make sure another application such as:

```text
Zoom
Teams
Google Meet
Camera
```

is not already using the webcam.

---

## TTS does not work

Run:

```powershell
python -c "import pyttsx3; e=pyttsx3.init(); e.say('Test'); e.runAndWait()"
```

Then check:

* Windows volume
* Application volume
* Default Windows audio output
* `pyttsx3` installation

---

## Object detector gives incorrect labels

Check:

1. Roboflow dataset labels
2. Dataset class names
3. Training quality
4. Model version
5. `ROBOFLOW_MODEL_ID`
6. Detection confidence
7. Lighting
8. Camera angle
9. Object size in the frame

Test the trained model in Roboflow before debugging the experiment logic.

---

## Video is lagging

Try:

* reducing camera resolution
* reducing AI inference frequency
* using a smaller model
* enabling GPU acceleration if available
* processing every 2nd/3rd frame

---

# 🔐 15. `.gitignore`

Do not upload your virtual environment, secrets, generated videos, logs or unnecessary model files.

Create:

```text
.gitignore
```

in the project root.

Recommended contents:

```gitignore
# Virtual environment
venv/
venv312/
.env

# Python cache
__pycache__/
*.py[cod]

# IDE
.vscode/

# Logs
data/logs/*
!data/logs/.gitkeep

# Recorded videos
data/videos/*
!data/videos/.gitkeep

# Local secrets
.env
*.key
*.secret

# Roboflow/API secrets
secrets.py

# Temporary files
*.tmp
*.temp

# OS files
.DS_Store
Thumbs.db
```

If your model files are very large, consider keeping them outside the normal Git repository or using Git LFS.

---

# 🐙 16. Upload Project to GitHub

Open the VS Code terminal in the project folder.

Check:

```powershell
git --version
```

Initialize Git:

```powershell
git init
```

Add files:

```powershell
git add .
```

Check what will be committed:

```powershell
git status
```

Commit:

```powershell
git commit -m "Initial commit"
```

Create a new repository on GitHub.

Then connect your local project:

```powershell
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Rename the branch:

```powershell
git branch -M main
```

Push:

```powershell
git push -u origin main
```

After the first push, future updates can usually be done with:

```powershell
git add .
git commit -m "Update project"
git push
```

---

# 🔒 IMPORTANT BEFORE `git push`

Run:

```powershell
git status
```

Make sure the following are NOT being uploaded:

```text
venv312/
.env
API keys
private credentials
large generated videos
large temporary files
```

Never put your Roboflow private API key directly into a public GitHub repository.

---

# 🧩 17. Adding a New Experiment

The system is designed so the experiment definition can be changed without rewriting the complete detection pipeline.

Define:

```text
Experiment
    ↓
Steps
    ↓
Objects
    ↓
Interaction conditions
    ↓
Expected order
```

For example:

```text
Step 1 → Pick up container
Step 2 → Open lid
Step 3 → Use spoon
Step 4 → Place material
Step 5 → Close container
```

The detection system identifies the objects and interactions while the sequence system determines whether the astronaut is following the expected order.

---

# 🛰️ 18. Intended BAS Use Case

The long-term concept is:

```text
Astronaut
    ↓
Fixed Payload Camera
    ↓
Local AI Processing
    ↓
Object + Pose Detection
    ↓
Experiment Step Recognition
    ↓
Sequence Validation
    ↓
Voice Feedback
    ↓
Timestamped Experiment Record
```

Instead of continuously sending raw video to Earth, the system can process the experiment locally and produce lightweight structured information about what happened.

---

# 🎯 Project Goals

The final system is intended to provide:

* Real-time experiment monitoring
* Object detection
* Human pose estimation
* Activity recognition
* Experiment sequence validation
* Missed-step detection
* Out-of-sequence detection
* Voice feedback
* Local video storage
* Timestamped event logs
* Offline operation
* Configurable experiments
* GUI monitoring

---

# ⚠️ Current Development Note

The object detection model is the foundation of the complete experiment-recognition pipeline.

Therefore, the development should proceed in this order:

```text
1. Verify camera
       ↓
2. Verify object detection
       ↓
3. Verify human pose detection
       ↓
4. Verify object + hand interaction
       ↓
5. Verify individual experiment conditions
       ↓
6. Verify step tracking
       ↓
7. Verify DAG/sequence validation
       ↓
8. Verify TTS alerts
       ↓
9. Verify logging
       ↓
10. Verify complete experiment
```

Do not attempt to tune all experiment steps simultaneously before the individual object classes are reliably detected.

---

# 📌 Quick Start

For an already configured project:

```powershell
cd "D:\New folder\BAS_based_HAR_system-main"
```

Activate the environment:

```powershell
venv312\Scripts\activate
```

Run:

```powershell
python main.py
```

Stop:

```text
Ctrl + C
```

---

# 👨‍💻 Development

This project is intended as a modular AI-based experiment-monitoring platform.

The detection layer, experiment-condition layer, sequence-validation layer, TTS layer, GUI layer and logging layer are separated so that individual components can be improved without redesigning the complete application.

---

# 📄 License

Add the project's chosen license here before publishing the repository publicly.

---

# 🚀 Future Improvements

Potential development areas include:

* Improved custom object detection
* Better hand-object interaction recognition
* More robust temporal activity recognition
* 3D/orientation-agnostic human pose estimation
* Better experiment configuration UI
* GPU acceleration
* More efficient edge inference
* Robust video streaming
* Automatic experiment report generation
* Additional BAS experiment templates
* Improved false-positive handling
* Confidence-aware step validation
* Multi-camera support

---

## Project Concept

**AI Human Activity Recognition for Autonomous On-Board BAS Experiments**

The system is intended to operate as an autonomous local AI assistant that monitors predefined scientific experiments, provides real-time feedback, detects deviations from the expected procedure and generates a lightweight record of the experiment.
