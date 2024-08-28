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
drop table if exists lh_fa_raw.my_first_dbt_model'''
spark.sql(sql)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sql = '''
        create table lh_fa_raw.my_first_dbt_model
      as
with source_data as (
    select 1 as id
    union all
    select null as id
)
select *
from source_data
-- where id is not null'''
spark.sql(sql)

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
# MAGIC drop table if exists lh_fa_raw.my_first_dbt_model

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC         create table lh_fa_raw.my_first_dbt_model
# MAGIC       as
# MAGIC with source_data as (
# MAGIC     select 1 as id
# MAGIC     union all
# MAGIC     select null as id
# MAGIC )
# MAGIC select *
# MAGIC from source_data
# MAGIC -- where id is not null

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
