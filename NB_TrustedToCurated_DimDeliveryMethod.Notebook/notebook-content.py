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

df_deliverymethods = spark.sql(f"select \
DeliveryMethodID as DeliveryMethodKey, \
DeliveryMethodName \
from LH_Trusted.application_deliverymethods D")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_deliverymethods = df_deliverymethods.withColumn("ETL_Curated", F.current_date())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_deliverymethods.write.mode("overwrite").format("delta").option("mergeSchema", "true").saveAsTable("LH_Curated.DimDeliveryMethods")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
