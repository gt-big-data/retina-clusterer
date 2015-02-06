# -*- coding: utf-8 -*-
import time
from db import app
import numpy as np

articleList = app.getPopulatedCount((time.time() - 100 * 86400))
# count = 0
# for article in articleList:
# 	count += 1
print articleList