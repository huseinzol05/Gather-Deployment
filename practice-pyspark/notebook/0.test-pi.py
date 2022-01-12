#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
import random
sc = pyspark.SparkContext(appName="Pi")


# In[1]:


from pyspark.sql import SparkSession


# In[3]:


spark = SparkSession     .builder     .appName('pi')     .master('spark://master:7077')     .getOrCreate()


# In[4]:


spark


# In[5]:


num_samples = 100000000


# In[8]:


import random

def inside(p):     
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, num_samples)).filter(inside).count()
pi = 4 * count / num_samples
print(pi)


# In[9]:


# !jupyter nbconvert --to script 0.test-pi.ipynb


# In[10]:


# !/opt/spark/bin/spark-submit \
#   --master spark://master:7077 \
#   /home/data/0.test-pi.py


# In[ ]:




