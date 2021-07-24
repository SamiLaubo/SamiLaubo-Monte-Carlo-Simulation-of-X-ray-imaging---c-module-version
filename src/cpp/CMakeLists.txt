cmake_minimum_required(VERSION "3.20.4")

project("Monte Carlo Simulation of X-ray imaging functions")

add_subdirectory(pybind11)

pybind11_add_module(cpp_funcs funcs.cpp)