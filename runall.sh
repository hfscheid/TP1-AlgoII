#!/usr/bin/env bash
for input in data/*
do
    echo $input >> error.txt
    (./run_xnn.py 4 8 12 16 24 28 32 $input) &>> error.txt
done
