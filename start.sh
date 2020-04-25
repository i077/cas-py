#! /bin/bash

python3 api.py &
pid=$!

trap "kill $pid" EXIT

cd frontend
yarn serve -s -l 3000 ./build
