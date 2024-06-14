cmake_minimum_required(VERSION 3.10)
project(TALON)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(include)

# Source files
set(SOURCES
    src/AxisAndAllies.cpp
    src/main.cpp
)

# Executable target
add_executable(TALON ${SOURCES})
