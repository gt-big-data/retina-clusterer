#!/bin/bash
cd /home/clusterer
echo $(date) >> clusterArticleRuns.log
python -m retina-clusterer.jobs.1-clusterArticles && echo $(date) >> clusterArticleSuccess.log
cd /home/clusterer/retina-clusterer
python db/nbCategories.py >> clusterNumberCategories.log
