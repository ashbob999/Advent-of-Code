cmake_minimum_required(VERSION 3.18)

project(aoc_2020_cpp)

set(CMAKE_CXX_STANDARD 20)

file(GLOB INPUT_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/input/*.txt
)

file(COPY ${INPUT_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/input)

include_directories(${SOURCE_DIR})
add_executable(aoc_2020_cpp "main.cpp" "../aocHelper.cpp" "../aocHelper.h" "day01.cpp" "day02.cpp" "day03.cpp" "day05.cpp" "day09.cpp" "day10.cpp" "day12.cpp" "day13.cpp" "day15.cpp" "day21.cpp" "day25.cpp" "day04.cpp" "day06.cpp" "day07.cpp" "day08.cpp" "day11.cpp" "day14.cpp" "day16.cpp" "day17.cpp" "day18.cpp" "day19.cpp" "day20.cpp" "day22.cpp" "day23.cpp" "day24.cpp")
