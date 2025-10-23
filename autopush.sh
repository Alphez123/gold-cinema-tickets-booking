#!/bin/bash
cd /path/to/your/project  # <-- replace with your full project path

while true
do
  git add .
  git commit -m "auto update $(date)"
  git push origin main
  sleep 60  # check every 60 seconds; change if you want faster/slower
done