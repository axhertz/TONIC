cmake_minimum_required(VERSION 3.15)
project(analyseQEPS)

set(CMAKE_CXX_STANDARD 17)

add_executable(analyseQEPS main.cpp Node.h Node.cpp)