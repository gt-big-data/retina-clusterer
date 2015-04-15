#!/bin/bash
cd /home/clusterer
echo $(date) >> keywordRuns.log
python -m retina-clusterer.jobs.2-extractKeywords && echo $(date) >> keywordSuccess.log
