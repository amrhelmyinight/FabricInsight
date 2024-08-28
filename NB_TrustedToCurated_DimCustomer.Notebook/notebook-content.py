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

df_customers = spark.sql(f"select \
CustomerID as CustomerKey, \
CustomerName, \
CustomerCategoryName, \
BuyingGroupName, \
CityName, \
StateProvinceName, \
SalesTerritory, \
CountryName, \
Continent, \
Region, \
SubRegion \
from LH_Trusted.sales_customers C \
left join \
LH_Trusted.sales_customercategories CC \
on CC.CustomerCategoryID = C.CustomerCategoryID \
left join \
LH_Trusted.sales_buyinggroups BG \
on BG.BuyingGroupID = C.BuyingGroupID \
left join \
LH_Trusted.application_cities CT \
on CT.CityID = C.DeliveryCityID \
left join \
LH_Trusted.application_stateprovinces SP \
on SP.StateProvinceID = CT.StateProvinceID \
left join \
LH_Trusted.application_countries CN \
on CN.CountryID = SP.CountryID")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customers = df_customers.withColumn("ETL_Curated", F.current_date())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customers.write.mode("overwrite").format("delta").option("mergeSchema", "true").saveAsTable("LH_Curated.DimCustomer")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
