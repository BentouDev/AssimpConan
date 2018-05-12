#!/bin/bash
conan remote add yage https://api.bintray.com/conan/bentoudev/yage

conan upload Assimp/0.1@bentoudev/yage --all -r=yage