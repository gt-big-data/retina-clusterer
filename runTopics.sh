#!/bin/bash
cd /home/clusterer
echo $(date) >> topicsRuns.log
export LD_LIBRARY_PATH=/usr/local/lib/
python -m retina-clusterer.3-dailyTopics && echo $(date) >> topicsSuccess.log
