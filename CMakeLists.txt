cmake_minimum_required(VERSION 3.10)
project(TALON)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

# Set the path to your LibTorch installation
set(Torch_DIR "/home/$USER/workspace/AxisAndAllies/libtorch/share/cmake/Torch")
find_package(Torch REQUIRED)


# Include directories
include_directories(include)
include_directories(${LIBTORCH_PATH}/include)
include_directories(${LIBTORCH_PATH}/include/torch/csrc/api/include)


# Source files
set(SOURCES
    src/AxisAndAllies.cpp
    src/main.cpp
)

# Executable target
add_executable(TALON ${SOURCES})

target_link_libraries(TALON "${TORCH_LIBRARIES}")
set_property(TARGET TALON PROPERTY CXX_STANDARD 17)