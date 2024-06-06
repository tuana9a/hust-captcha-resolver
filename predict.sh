#!/bin/bash

predictUrl=${predictUrl:-https://hcr.tuana9a.com}

filepath=$1

echo "$filepath -> $predictUrl -> $(curl -s -X POST "$predictUrl" -F "file=@$filepath")";
