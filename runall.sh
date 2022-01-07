#!/usr/bin/env bash
echo '' > error.txt
for input in data/*
do
    echo $input >> error.txt
    (./run_xnn.py 4 8 12 16 20 24 28 32 36 40 44 48 52 56 60 64 $input) &>> error.txt
done
