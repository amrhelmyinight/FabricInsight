# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": "",
# META       "known_lakehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 📌 Attach Default Lakehouse
# ❗**Note the code in the cell that follows is required to programatically attach the lakehouse and enable the running of spark.sql(). If this cell fails simply restart your session as this cell MUST be the first command executed on session start.**

# CELL ********************

# MAGIC %%configure
# MAGIC {
# MAGIC     "defaultLakehouse": {  
# MAGIC         "name": "lh_fa_raw",
# MAGIC     }
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # 📦 Pip
# Pip installs reqired specifically for this template should occur here

# CELL ********************

# No pip installs needed for this notebook

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # 🔗 Imports

# CELL ********************

from notebookutils import mssparkutils # type: ignore
from pyspark.sql.types import StructType, StructField, StringType, BooleanType
from dataclasses import dataclass
import json
import hashlib

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # { } Params

# CELL ********************

# Set Lakehouse
RelativePathForMetaData = "Files/MetaExtracts/"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # #️⃣ Functions

# CELL ********************

def execute_sql_and_write_to_file(sql_query, file_path):
    # Execute the SQL query
    df = spark.sql(sql_query) # type: ignore
    df_to_file(df, file_path)

def df_to_file(df, file_path):

    # Convert the DataFrame to a Pandas DataFrame
    pandas_df = df.toPandas()

    # Convert the Pandas DataFrame to a string
    df_string = pandas_df.to_json(None, orient='records')

    # Write the string to the file
    mssparkutils.fs.put(file_path, df_string, True) # type: ignore

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # List Schemas Macro Export

# CELL ********************

execute_sql_and_write_to_file("show databases", f"{RelativePathForMetaData}/ListSchemas.json")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # List Relations

# CELL ********************

# Define the schema
schema = StructType([
    StructField("namespace", StringType(), True),
    StructField("tableName", StringType(), True),
    StructField("isTemporary", BooleanType(), True),
    StructField("information", StringType(), True)
])

# Create an empty DataFrame with the schema
union_df = spark.createDataFrame([], schema) # type: ignore

df = spark.sql("show databases") # type: ignore
for row in df.collect():
    sql = f"show table extended in {row['namespace']} like '*'"
    df_temp = spark.sql(sql) # type: ignore
    
    #display(df_temp)
    union_df = union_df.union(df_temp)

df_to_file(union_df, f"{RelativePathForMetaData}/ListRelations.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Describe Table Extended

# CELL ********************

import json
from pyspark.sql.types import StructType, StructField, StringType, BooleanType # type: ignore
from pyspark.sql.functions import lit # type: ignore


# Define the schema
schema = StructType([
    StructField("col_name", StringType(), True),
    StructField("data_type", StringType(), True),
    StructField("comment", StringType(), True), 
    StructField("namespace", StringType(), True),
    StructField("tableName", StringType(), True),
])


# Create an empty DataFrame with the schema
union_df = spark.createDataFrame([], schema) # type: ignore

data = spark.sparkContext.wholeTextFiles(f"{RelativePathForMetaData}/ListRelations.json").collect() # type: ignore
file_content = data[0][1]
jo = json.loads(file_content)
for j in jo:
    sql = f"use { j['namespace'] }"
    spark.sql(sql) # type: ignore
    sql = f"describe extended { j['tableName'] }"
    df_temp = spark.sql(sql) # type: ignore
    
    df_temp = df_temp.withColumn('namespace', lit(j['namespace']))
    df_temp = df_temp.withColumn('tableName', lit(j['tableName']))
    
    union_df = union_df.union(df_temp)

df_to_file(union_df, f"{RelativePathForMetaData}/DescribeRelations.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # #️⃣ Create Hash for Files 

# CELL ********************

# Define the schema
schema = StructType([
    StructField("hash", StringType(), True),
    StructField("file", StringType(), True)
])

files = ["ListSchemas","DescribeRelations","ListRelations"]

df = spark.createDataFrame([], schema) # type: ignore
for file in files:
    data = spark.sparkContext.wholeTextFiles(f"{RelativePathForMetaData}/{file}.json").collect() # type: ignore
    file_content = data[0][1]
    hashinfo = {}
    hashinfo['hash'] = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
    hashinfo['file'] = f"{file}.json"
    df = df.union(spark.createDataFrame([hashinfo])) # type: ignore
    
df_to_file(df, f"{RelativePathForMetaData}/MetaHashes.json") # type: ignore


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
