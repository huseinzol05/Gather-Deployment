#!/usr/bin/env python
# coding: utf-8

# In[14]:


from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.types import *

warehouse_location = 'hdfs://hdfs:9000/hive/warehouse'


# In[19]:


schema = StructType([StructField('Id', IntegerType(), True),
           StructField('SepalLengthCm', DoubleType(), True),
           StructField('SepalWidthCm', DoubleType(), True),
           StructField('PetalLengthCm', DoubleType(), True),
           StructField('PetalWidthCm', DoubleType(), True),
           StructField('Species', StringType(), True)])


# In[2]:


spark = SparkSession     .builder     .appName("Python Spark SQL Hive integration example")     .config("spark.sql.warehouse.dir", warehouse_location)     .enableHiveSupport()     .getOrCreate()


# In[3]:


spark.sql("CREATE TABLE IF NOT EXISTS iris (Id INT, SepalLengthCm DOUBLE, SepalWidthCm DOUBLE, PetalLengthCm DOUBLE, PetalWidthCm DOUBLE, Species STRING) USING hive")


# In[20]:


df = spark.read.format("CSV").option("header","true").schema(schema).load('hdfs://hdfs:9000/user/Iris.csv')


# In[21]:


df.show()


# In[22]:


df.dtypes


# In[23]:


df.write.insertInto('iris')


# In[25]:


spark.sql('select max(PetalWidthCm) from iris').show()

