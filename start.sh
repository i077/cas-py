#! /bin/bash

python3 api.py &
pid=$!

trap "kill $pid" EXIT

cd frontend

if [ ! -d "./build" ] 
then
    yarn build .
fi

yarn serve -s -l 3000 ./build
