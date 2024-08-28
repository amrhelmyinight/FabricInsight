# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
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

# # #️⃣ Parameters

# PARAMETERS CELL ********************

pm_batch_id = None

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # 📦 Pip
# Pip installs reqired specifically for this template should occur here

# CELL ********************

!pip install jsonpickle

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # 🔗 Imports

# CELL ********************

from notebookutils import mssparkutils # type: ignore
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import json
import time
import jsonpickle # type: ignore
import json
from pyspark.sql.types import *
from pyspark.sql.functions import *
import os

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # #️⃣ Functions

# CELL ********************

notebook_files1 = ['model.amr_project.my_second_dbt_model', 'test.amr_project.not_null_my_first_dbt_model_id.5fb22c2710', 'test.amr_project.unique_my_first_dbt_model_id.16e066b321']
run_order1 = 1

# Define a function to execute a notebook and return the results
@dataclass
class NotebookResult:    
    notebook: str
    start_time: float
    status: str
    error: str
    execution_time: float
    run_order: int

def execute_notebook(notebook_file):
    start_time = time.time()

    try:
        mssparkutils.notebook.run(notebook_file)
        status = 'success'
        error = None
    except Exception as e:
        status = 'error'
        error = str(e)

    execution_time = time.time() - start_time
    run_order = run_order1

    result = NotebookResult(notebook_file, start_time, status, error, execution_time,run_order)
    return result

@dataclass
class FileListing:
    """Class for Files - Attributes: name, directory"""
    name: str
    directory: str

def get_file_content_using_notebookutils(file):
    """Get the content of a file using notebookutils."""
    #return self.mssparkutils.fs.head(file, 1000000000)
    data = spark.sparkContext.wholeTextFiles(file).collect() # type: ignore

    # data is a list of tuples, where the first element is the file path and the second element is the content of the file
    file_content = data[0][1]

    return file_content

def create_path_using_notebookutils(path):
    """Create a path using notebookutils."""
    mssparkutils.fs.mkdirs(path)

def walk_directory_using_notebookutils(path):
    """Walk a directory using notebookutils."""
    # List the files in the directory
    files = mssparkutils.fs.ls(path)

    # Initialize the list of all files
    all_files = []

    # Iterate over the files
    for file in files:
        # If the file is a directory, recursively walk the directory
        if file.isDir:
            all_files.extend(
                walk_directory_using_notebookutils(file.path))
        else:
            # If the file is not a directory, add it to the list of all files
            directory = os.path.dirname(file.path)
            name = file.name
            all_files.append(FileListing(
                name=name, directory=directory))

    return all_files


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Load the Execution Log


# CELL ********************

# Define the schema for the DataFrame
schema = StructType([
    StructField("notebook", StringType(), True),
    StructField("start_time", DoubleType(), True),
    StructField("status", StringType(), True),
    StructField("error", StringType(), True),
    StructField("execution_time", DoubleType(), True),
    StructField("run_order", IntegerType(), True),
    StructField("batch_id", StringType(), True)
])

# Create an empty DataFrame with the defined schema
failed_results = spark.createDataFrame([], schema=schema)
# Read the log for this batch execution
df_execution_log = spark.sql(f"SELECT * FROM lh_fa_raw.execution_log WHERE batch_id = '{pm_batch_id}'")
if df_execution_log.count() > 0:
    
    # Check if any have not succeeded
    failed_results = df_execution_log.filter(col("status") != "success")

    # Print the failed results
    for row in failed_results.collect():
        print(f"Notebook {row['notebook']} failed with error: {row['error']}")

    # Check if have succeeded
    succeeded_results = df_execution_log.filter(col("status") == "success")

    # Print the succeeded results
    for row in succeeded_results.collect():
        print(f"Notebook {row['notebook']} succeeded")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Execute Notebooks 

# CELL ********************

# Define the schema for the Log DataFrame
schema = StructType([
    StructField("notebook", StringType(), True),
    StructField("start_time", DoubleType(), True),
    StructField("status", StringType(), True),
    StructField("error", StringType(), True),
    StructField("execution_time", DoubleType(), True),
    StructField("run_order", IntegerType(), True)
])

if failed_results.count() == 0:
    new_results = []
    # Use a ThreadPoolExecutor to run the notebooks in parallel
    # Execute the notebooks and collect the results
    with ThreadPoolExecutor(max_workers=5) as executor:
        new_results = list(executor.map(execute_notebook, notebook_files1))

    # Write the results to the log file
    df_log = spark.createDataFrame(new_results, schema=schema)
    df_log = df_log.withColumn("batch_id", lit(f'{pm_batch_id}'))
    df_log.write.format("delta").mode("append").saveAsTable("lh_fa_raw.execution_log")
else:
    print("Failures in previous run_order... supressing execution")
    raise Exception("Failures in previous run_order... supressing execution")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
