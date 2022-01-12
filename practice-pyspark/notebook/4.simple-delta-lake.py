#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyspark
from delta import *


# In[2]:


warehouse_location = 'hdfs://hdfs:9000/hive/warehouse'


# In[3]:


builder = pyspark.sql.SparkSession.builder.appName("MyApp")     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")     .config("spark.sql.warehouse.dir", warehouse_location)

spark = configure_spark_with_delta_pip(builder).getOrCreate()


# In[4]:


spark


# In[5]:


path = 'hdfs://hdfs:9000/user/range-temp-table'


# In[6]:


data = spark.range(0, 5)
data.write.format('delta').mode('overwrite').save(path)


# In[7]:


df = spark.read.format('delta').load(path)
df.show()


# In[8]:


data = spark.range(5, 10)
data.write.format('delta').mode('overwrite').save(path)


# In[9]:


from delta.tables import *
from pyspark.sql.functions import *

deltaTable = DeltaTable.forPath(spark, path)
deltaTable


# In[10]:


deltaTable.update(
  condition = expr("id % 2 == 0"),
  set = { "id": expr("id + 100") })


# In[11]:


deltaTable.toDF().show()


# In[12]:


deltaTable.delete(condition = expr("id % 2 == 0"))


# In[13]:


deltaTable.toDF().show()


# In[14]:


newData = spark.range(0, 20)

deltaTable.alias("oldData")   .merge(
    newData.alias("newData"),
    "oldData.id = newData.id") \
  .whenMatchedUpdate(set = { "id": col("newData.id") }) \
  .whenNotMatchedInsert(values = { "id": col("newData.id") }) \
  .execute()


# In[15]:


deltaTable.toDF().show()


# In[16]:


deltaTable.toDF().write.format('delta').mode('overwrite').save(path)


# In[17]:


deltaTable = DeltaTable.forPath(spark, path)
deltaTable.toDF().show()


# In[18]:


# !jupyter nbconvert --to script 4.simple-delta-lake.ipynb


# In[19]:


# !/opt/spark/bin/spark-submit \
#   --master spark://master:7077 \
#   /home/data/4.simple-delta-lake.py


# In[ ]:




