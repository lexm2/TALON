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

3. Create a Virtual Environment (venv):
Use green for linux/mac and red for windows.
```diff
python -m venv .venv
+ source .venv/bin/activate
- .venv\Scripts\activate
pip install torch Numpy
```
When you're done working with the virtual environment, you can deactivate it by running the following command.
`deactivate`

3. Navigate to the build directory and generate the build files using CMake:
``` 
cd build
cmake ..
make
```