#!/bin/bash
cd /home/clusterer
echo $(date) >> keywordRuns.log
python -m retina-clusterer.1-extractKeywords && echo $(date) >> keywordSuccess.log
