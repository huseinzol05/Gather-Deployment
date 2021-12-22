#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
from pyspark import SQLContext


# In[2]:


sc = pyspark.SparkContext(appName="sql")


# In[3]:


sqlcontext = SQLContext(sc)


# In[4]:


simpleData = [("James", "Sales", 3000),
    ("Michael", "Sales", 4600),
    ("Robert", "Sales", 4100),
    ("Maria", "Finance", 3000),
    ("James", "Sales", 3000),
    ("Scott", "Finance", 3300),
    ("Jen", "Finance", 3900),
    ("Jeff", "Marketing", 3000),
    ("Kumar", "Marketing", 2000),
    ("Saif", "Sales", 4100)
  ]
schema = ['employee_name', 'department', 'salary']

df = sqlcontext.createDataFrame(data=simpleData, schema = schema)


# In[5]:


df.show()


# In[14]:


from pyspark.sql.functions import max


# In[16]:


max('salary')


# In[17]:


df.select(max('salary')).show()


# In[21]:


# !jupyter nbconvert --to script 1.sql.ipynb


# In[20]:


# !/opt/spark/bin/spark-submit \
#   --master spark://172.20.0.3:7077 \
#   /home/data/1.sql.py


# In[ ]:




