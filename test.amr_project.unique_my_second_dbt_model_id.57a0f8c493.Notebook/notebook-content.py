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

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # #️⃣ Functions

# CELL ********************

# No Functions needed for this notebook


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Declare and Execute SQL Statements

# CELL ********************

sql = '''
select
      INT(count(*)) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
select
    id as unique_field,
    count(*) as n_records
from lh_fa_raw.my_second_dbt_model
where id is not null
group by id
having count(*) > 1
    ) dbt_internal_test'''
spark.sql(sql)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Execute SQL 

# CELL ********************

# Execute the SQL query
df = spark.sql(sql)

# Get the first row of the DataFrame
row = df.first()

# Check if failures or should_error are greater than 0
if row.failures > 0 or row.should_error:
    raise ValueError('Failures or should_error are greater than 0')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # 🛑 Execution Stop

# CELL ********************

#Exit to prevent spark sql debug cell running 
mssparkutils.notebook.exit("value string")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # SPARK SQL Cells for Debugging

# CELL ********************

# MAGIC %%sql
# MAGIC select
# MAGIC       INT(count(*)) as failures,
# MAGIC       count(*) != 0 as should_warn,
# MAGIC       count(*) != 0 as should_error
# MAGIC     from (
# MAGIC select
# MAGIC     id as unique_field,
# MAGIC     count(*) as n_records
# MAGIC from lh_fa_raw.my_second_dbt_model
# MAGIC where id is not null
# MAGIC group by id
# MAGIC having count(*) > 1
# MAGIC     ) dbt_internal_test

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
