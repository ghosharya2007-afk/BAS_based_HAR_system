Into SpaceTech, where resource is scarce.

Tech Stack: 

# A-EYE

Into SpaceTech, where resources are scarce.

- Python 3.11
- PyTorch 2.3.1
- Torchvision 0.18.1
- OpenCV 4.10.0.84
- MediaPipe 0.10.14
- NumPy 1.26.4
- Scikit-learn 1.5.1
- JupyterLab 4.2.5

## Installation in VS Code

Open the VS Code terminal with **Ctrl + `**, then run:

### Clone the repository

```powershell
git clone https://github.com/Anish05s/BAS_based_HAR_system
cd <File-name>

Create and activate a virtual environment

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

Install the dependencies

python -m pip install --upgrade pip
pip install torch==2.3.1 torchvision==0.18.1
pip install opencv-python==4.10.0.84 mediapipe==0.10.14 numpy==1.26.4 scikit-learn==1.5.1 jupyterlab==4.2.5

Run the project

python main.py

To launch JupyterLab: 

jupyter lab

In VS Code, select the virtual environment as the Python interpreter:

Ctrl + Shift + P → Python: Select Interpreter → .venv


Relevant researcher work:

1. Carreira & Zisserman (2017) — "Quo Vadis, Action Recognition?" (I3D) — CVPR 2017. Multi-scale 3D ConvNets for video action recognition. Foundational for sequence-based HAR.
2. Yan et al. (2018) — "Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition" (ST-GCN) — AAAI 2018. Treats skeleton joints as graph → GCN for action classification. Direct fit for your use case.
3. Cheng et al. (2020) — "Skeleton-based Action Recognition with Shift Graph Convolutional Network" (Shift-GCN). Improved over ST-GCN. Handles variable sequence lengths.
4. NASA EVA task monitoring — Unpublished internal work on real-time astronaut activity tracking in spacesuits.


