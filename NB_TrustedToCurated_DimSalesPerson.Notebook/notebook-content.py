# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4fbce8f0-c2f5-479a-94a6-d9348a9d225d",
# META       "default_lakehouse_name": "LH_Trusted",
# META       "default_lakehouse_workspace_id": "ece02e6c-3fca-4522-b360-fb40feb0b364"
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F
import datetime

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_salesperson = spark.sql(f"select \
PersonID as SalesPersonKey, \
FullName \
from LH_Trusted.application_people \
where IsSalesperson = 1")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_salesperson = df_salesperson.withColumn("ETL_Curated", F.current_date())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_salesperson.write.mode("overwrite").format("delta").option("mergeSchema", "true").saveAsTable("LH_Curated.DimSalesPerson")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
