#!/bin/bash
cd /home/clusterer/retina-clusterer
while true
do
python 2-extractKeywords.py && echo $(date) >> keywordSuccess.log
sleep 1
done
