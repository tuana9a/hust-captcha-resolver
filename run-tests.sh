#!/bin/bash

filepaths=./samples/*

predictUrl=${predictUrl:-https://hcr.tuana9a.com}

for filepath in $filepaths; do
    echo "$filepath -> $predictUrl -> $(curl -s -X POST "$predictUrl" -F "file=@$filepath")";
done