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

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_Invoices = spark.sql(f"select \
        SI.CustomerID as CustomerKey, \
        SI.BillToCustomerID as BillToCustomerKey, \
        SI.DeliveryMethodID as DeliveryMethodKey, \
        SI.OrderID, \
        SI.InvoiceID, \
        SIL.InvoiceLineID, \
        SI.SalespersonPersonID as SalespersonPersonKey, \
        SI.InvoiceDate, \
        SI.CustomerPurchaseOrderNumber, \
        SI.IsCreditNote, \
        SI.CreditNoteReason, \
        SIL.StockItemID as StockItemKey, \
        SIL.Quantity, \
        SIL.UnitPrice, \
        SIL.TaxRate, \
        SIL.TaxAmount, \
        SIL.LineProfit, \
        SIL.ExtendedPrice \
    from \
        LH_Trusted.sales_invoices SI \
    join \
        LH_Trusted.sales_invoicelines SIL \
    on \
        SIL.InvoiceID = SI.InvoiceID ")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_Invoices = df_Invoices.withColumn("InvoiceDateKey", date_format(col("InvoiceDate"), "yyyyMMdd").cast("int"))
df_Invoices = df_Invoices.drop("InvoiceDate")

df_Invoices = df_Invoices.withColumn("SalesAmount", col("Quantity") * col("UnitPrice"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_Invoices = df_Invoices.withColumn("ETL_Curated", F.current_date())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_Invoices.write.mode("overwrite").format("delta").saveAsTable("LH_Curated.FactSales")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
