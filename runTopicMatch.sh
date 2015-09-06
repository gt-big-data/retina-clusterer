#!/bin/bash
cd /home/clusterer
echo $(date) >> topics2Runs.log
export LD_LIBRARY_PATH=/usr/local/lib/
python -m retina-clusterer.4-topicMatch && echo $(date) >> topics2Success.log