#!/bin/sh

cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=./toolchain.cmake -S . -B dist
cmake --build dist