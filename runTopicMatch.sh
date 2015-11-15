#!/bin/bash
cd /home/clusterer/retina-clusterer
echo $(date) >> topics2Runs.log
export LD_LIBRARY_PATH=/usr/local/lib/
python 2-topicMatch.py && echo $(date) >> topics2Success.log
