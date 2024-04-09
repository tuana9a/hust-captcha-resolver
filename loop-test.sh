#!/bin/bash

if [ -z "$PREDICT_URL" ]; then
  PREDICT_URL=https://hcr.tuana9a.com
fi

while true; do
  for f in ./samples/*.png; do
    echo -n "$f -> "; curl -X POST "$PREDICT_URL" -F "file=@$f"
    echo
  done
done
