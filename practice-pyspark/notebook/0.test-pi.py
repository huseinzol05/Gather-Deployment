#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
import random
sc = pyspark.SparkContext(appName="Pi")
num_samples = 100000000


# In[2]:


def inside(p):     
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(range(0, num_samples)).filter(inside).count()
pi = 4 * count / num_samples
print(pi)
sc.stop()


# In[ ]:




