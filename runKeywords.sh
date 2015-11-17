#!/bin/bash
cd /home/clusterer/retina-clusterer
echo $(date) >> keywordRuns.log
python 1-extractKeywords.py && echo $(date) >> keywordSuccess.log
