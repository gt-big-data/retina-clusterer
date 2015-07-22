#!/bin/bash
cd /home/clusterer
echo $(date) >> topics2Runs.log
python -m retina-clusterer.jobs.4-topicMatch && echo $(date) >> topics2Success.log
