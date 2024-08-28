# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "cbda9fc4-08ba-43ab-801f-bde75611ae9f",
# META       "default_lakehouse_name": "lh_fa_amr_raw",
# META       "default_lakehouse_workspace_id": "ece02e6c-3fca-4522-b360-fb40feb0b364"
# META     }
# META   }
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
from pyspark.sql.functions import lower
from dataclasses import dataclass
import json
import hashlib
import yaml


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

#convert database/ lakehouse name to lower case
#execute_sql_and_write_to_file("show databases", f"{RelativePathForMetaData}/ListSchemas.json")
df_database = spark.sql("show databases")
df_database = df_database.withColumn('namespace', lower(df_database['namespace']))

df_to_file (df_database, f"{RelativePathForMetaData}/ListSchemas.json")

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

#convert database/ lakehouse name and table name to lower case
union_df = union_df.withColumn('namespace', lower(union_df['namespace']))
union_df = union_df.withColumn('tableName', lower(union_df['tableName']))

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
union_dtable = spark.createDataFrame([], schema) # type: ignore

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
    
    # generate Schema.yml
    sqldesc = f"describe { j['tableName'] }"
    df_dtable = spark.sql(sqldesc) # type: ignore
    df_dtable = df_dtable.withColumn('namespace', lower(lit(j['namespace'])))
    df_dtable = df_dtable.withColumn('tableName', lower(lit(j['tableName'])))
    union_dtable = union_dtable.union(df_dtable)

#convert column name to lower case
union_df = union_df.withColumn('col_name', lower(union_df['col_name']))
union_dtable = union_dtable.withColumn('col_name', lower(union_dtable['col_name']))
union_dtable.createOrReplaceTempView("describetable")
df_to_file(union_df, f"{RelativePathForMetaData}/DescribeRelations.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Schema yaml generation

# CELL ********************

tables = {}
for item in union_dtable.collect():
    #print(item)
    table_name = item['tableName']
    col_name = item['col_name']
    
    if table_name not in tables:
        tables[table_name] = []
    
    if col_name:  # Only add columns with a name
        tables[table_name].append({
            "name": col_name,
            "description": "add column description"
        })

output_data = {}
output_data["version"] = 2
models = []
for table_name, columns in tables.items():
    models.append({
        "name": table_name,
        "description": "add table description",
        "columns": columns
    })
output_data["models"] = models

yaml_string = yaml.dump(output_data,  default_flow_style=False)
RelativePathForShemaTemplate = "Files/SchemaTemplate"
file_path = f"{RelativePathForShemaTemplate}/schema.yml"
mssparkutils.fs.put(file_path, yaml_string, True) # type: ignore

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
    df = df.union(spark.createDataFrame([hashinfo], schema)) # type: ignore
    
df_to_file(df, f"{RelativePathForMetaData}/MetaHashes.json") # type: ignore


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
