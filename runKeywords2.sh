#!/bin/bash
cd /home/clusterer
while true
do
python -m retina-clusterer.2-extractKeywords && echo $(date) >> keywordSuccess.log
sleep 1
done
