#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession


# In[2]:


sparkSession = SparkSession.builder.appName("csv").getOrCreate()


# In[5]:


df = sparkSession.read.format("CSV").option("header","true").load('hdfs://hdfs:9000/user/Iris.csv')
df.show()


# In[7]:


from pyspark.sql.functions import max


# In[8]:


df.select(max('SepalLengthCm')).show()


# In[12]:


# !jupyter nbconvert --to script 2.simple-hdfs.ipynb


# In[13]:


# !/opt/spark/bin/spark-submit \
#   --master spark://172.20.0.3:7077 \
#   /home/data/2.simple-hdfs.py


# In[ ]:




