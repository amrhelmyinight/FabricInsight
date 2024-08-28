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

def pre_execute_notebook(notebook_file):

    try:
        mssparkutils.notebook.run(notebook_file)
        status = 'PreExecute Notebook Executed'
        error = None
    except Exception as e:
        status = 'No PreExecute Notebook Found'
        error = str(e)

    return status

def post_execute_notebook(notebook_file):

    try:
        mssparkutils.notebook.run(notebook_file)
        status = 'PostExecute Notebook Executed'
        error = None
    except Exception as e:
        status = 'No PostExecute Notebook Found'
        error = str(e)

    return status

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Declare and Execute Pre-Execution Notebook

# CELL ********************

#Read the context of the notebook
notebook_info = mssparkutils.runtime.context

# Extract the currentNotebookName from the dictionary
current_notebook_name = notebook_info.get("currentNotebookName")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Execute Pre-Execute Notebook
preexecute_notebook_name  = current_notebook_name+ ".preexecute"
pre_execute_notebook(preexecute_notebook_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Declare and Execute SQL Statements

# CELL ********************

sql = '''
drop table if exists lh_fa_amr_raw.my_first_dbt_model'''
spark.sql(sql)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sql = '''
        create table lh_fa_amr_raw.my_first_dbt_model
      as
with source_data as (
    select 1 as id
    union all
    select 4 as id
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

# Execute Post-Execute Notebook
postexecute_notebook_name  = current_notebook_name + ".postexecute"
post_execute_notebook(postexecute_notebook_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

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
# MAGIC drop table if exists lh_fa_amr_raw.my_first_dbt_model

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC         create table lh_fa_amr_raw.my_first_dbt_model
# MAGIC       as
# MAGIC with source_data as (
# MAGIC     select 1 as id
# MAGIC     union all
# MAGIC     select 4 as id
# MAGIC )
# MAGIC select *
# MAGIC from source_data
# MAGIC -- where id is not null

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
