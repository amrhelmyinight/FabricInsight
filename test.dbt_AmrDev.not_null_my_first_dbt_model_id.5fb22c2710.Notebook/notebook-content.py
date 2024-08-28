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
select id
from lh_fa_amr_raw.my_first_dbt_model
where id is null
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
# MAGIC select id
# MAGIC from lh_fa_amr_raw.my_first_dbt_model
# MAGIC where id is null
# MAGIC     ) dbt_internal_test

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
