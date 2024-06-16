cmake_minimum_required(VERSION 3.10)
project(TALON)

set(LIBTORCH_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libtorch")

find_package(Torch REQUIRED PATHS "${LIBTORCH_DIR}")

# Include directories
include_directories(${TORCH_INCLUDE_DIRS})
include_directories(include)

set(SOURCES
    src/main.cpp
    src/NeuralNetwork.cpp
    src/Game/Game.cpp
)

# Executable target
add_executable(TALON ${SOURCES})
target_link_libraries(TALON "${TORCH_LIBRARIES}")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)