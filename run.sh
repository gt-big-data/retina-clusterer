#!/bin/bash
echo $(date) >> runs.log
python cluster_update.py && echo $(date) >> success.log
python db/nbCategories.py >> clusterSize.log
