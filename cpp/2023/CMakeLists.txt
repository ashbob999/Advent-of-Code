cmake_minimum_required(VERSION 3.18)

project(aoc_2023_cpp)

set(CMAKE_CXX_STANDARD 20)

file(GLOB INPUT_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/input/*.txt
)

file(COPY ${INPUT_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/input)

if (MSVC) # windows msvc
	set(LLVM_DIR ./../llvm-project/build-msvc/lib/cmake/llvm)

	if (CMAKE_BUILD_TYPE EQUAL "DEBUG")
		add_compile_options(/MTd)
	else()
		add_compile_options(/MT)
	endif()
endif()

find_package(Z3 CONFIG REQUIRED)

include_directories(${SOURCE_DIR})

add_executable(aoc_2023_cpp "main.cpp" "../aocHelper.h" "day01.cpp" "day24.cpp")

target_link_libraries(aoc_2023_cpp PRIVATE z3::libz3)
