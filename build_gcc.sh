#!/bin/bash
export CXX=g++
export CC=gcc
$CXX --version
cmake --version
conan --version
conan create . bentoudev/yage -s compiler=gcc compiler.libcxx=libstdc++
