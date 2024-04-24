#!/bin/bash

if [ -z "$PREDICT_URL" ]; then PREDICT_URL=https://hcr.tuana9a.com; fi

filepath=$1

echo "$filepath -> $(curl -X POST "$PREDICT_URL" -F "file=@$filepath")";
