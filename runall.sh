#!/usr/bin/env bash
echo '' > error.txt
for input in data/*
do
    echo $input >> error.txt
    (./run_xnn.py 4 $input) &>> error.txt
done
