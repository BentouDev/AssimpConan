#!/bin/bash
export CXX=g++
export CC=gcc
$CXX --version
cmake --version
conan --version
conan create . bentoudev/yage