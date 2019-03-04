cmake_minimum_required(VERSION 3.11)

project(IntegrationTest VERSION 1.8.9)

add_executable(it Main.cpp)
target_link_libraries(it PRIVATE lib)
