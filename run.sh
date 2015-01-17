#!/bin/bash
python cluster_update.py
echo $(date) >> runs.log
python db/nbCategory.py >> clusterSize.log