#!/bin/bash
cd /home/clusterer
echo $(date) >> topicsRuns.log
python -m retina-clusterer.jobs.3-dailyTopics && echo $(date) >> topicsSuccess.log
