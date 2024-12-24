cmake_minimum_required(VERSION 3.18)

project(aoc_2024_cpp)

set(CMAKE_CXX_STANDARD 20)

file(GLOB INPUT_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/../../2024/input/*.txt
)

file(COPY ${INPUT_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/input)

include_directories(${SOURCE_DIR})

add_executable(aoc_2024_cpp "main.cpp" "../aocHelper.h" "day01.cpp")
