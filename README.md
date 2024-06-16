# AxisAndAllies

AxisAndAllies is game implemented in C++ that uses live training with a Python server. The game communicates with the server to get the AI's moves and sends game states for training.

## Prerequisites

Before running the game, make sure you have the following dependencies installed:

- C++ compiler (e.g., g++, gcc)
- Python 3
- CMake

## Setup

1. Clone the repository or download the source code files.

2. Open a terminal or command prompt and navigate to the project's root directory.

3. Update and upgrade package manager and build essentials:
```
sudo apt update
sudo apt upgrade
sudo apt install build-essential cmake
```

3. Install CUDA:
Visit the NVIDIA CUDA website: https://developer.nvidia.com/cuda-downloads
Select the appropriate operating system (Linux), architecture (x86_64), distribution (Ubuntu), and version (e.g., 22.04).

Verify Installation
``` 
nvcc --version
```

4. Install cuDNN:
Visit the NVIDIA cuDNN website: https://developer.nvidia.com/cudnn
Download the cuDNN library compatible with your CUDA version.

5. Set up project:
```
mkdir build
cd build
cmake ..
make
```