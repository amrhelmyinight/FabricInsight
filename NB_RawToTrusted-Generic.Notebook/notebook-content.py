# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ec0859fb-7523-4622-8af3-665f5b58ca6c",
# META       "default_lakehouse_name": "LH_Raw",
# META       "default_lakehouse_workspace_id": "ece02e6c-3fca-4522-b360-fb40feb0b364"
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

# parameters
InputRawBlobFile = "POC/2024/05/03/sales_customers.csv"
OutputTrustedBlobFile = "POC/sales_customers"
OutputTrustedFileFormat = "BLOB Storage (deltalake)"
OutputTrustedFileWriteMode = "overwrite"
KeyColumns = "CustomerID"
ToDateColumns = ""
NullConversionColumns = ""
RenameColumns = ""
TargetName = "sales_customers"
Workspace = "POC"
Raw_Lakehouse = "LH_Raw"
Trusted_Lakehouse = "LH_Trusted"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Fix missing param
TimeZone = "Australia/Sydney"

# Fix Input File
InputRawBlobFile = "Files/"+InputRawBlobFile

print(InputRawBlobFile)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run NB_KeyVaultFunctions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run NB_StorageFunctions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run NB_TransformationFunctions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Import References

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.window import *
from delta.tables import *
import datetime
import pytz

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Parameters

# CELL ********************

# Set Parameters
#dbutils.widgets.removeAll()

#dbutils.widgets.text("TimeZone","Australia/Sydney")

#dbutils.widgets.text("InputRawBlobFile", "")

#dbutils.widgets.text("OutputTrustedBlobFile", "")
#dbutils.widgets.dropdown(name="OutputTrustedFileFormat", defaultValue="BLOB Storage (deltalake)", choices=["BLOB Storage (csv)", "BLOB Storage (parquet)", "BLOB Storage (orc)", "BLOB Storage (json)", "BLOB Storage (deltalake)"]) 
#dbutils.widgets.dropdown(name="OutputTrustedFileWriteMode", defaultValue="upsert", choices=["upsert", "delete-insert", "append", "overwrite", "ignore", "error", "errorifexists"]) 

#dbutils.widgets.text("KeyColumns", "")
#dbutils.widgets.text("RenameColumns", "")
#dbutils.widgets.text("ToDateColumns", "")
#dbutils.widgets.text("NullConversionColumns", "")

# Get Parameters
#timeZone = dbutils.widgets.get("TimeZone")

#inputRawBlobFile = dbutils.widgets.get("InputRawBlobFile")

#outputTrustedBlobFile = dbutils.widgets.get("OutputTrustedBlobFile")
#outputTrustedFileFormat = dbutils.widgets.get("OutputTrustedFileFormat")
#outputTrustedFileWriteMode = dbutils.widgets.get("OutputTrustedFileWriteMode")

#keyColumns  = dbutils.widgets.get("KeyColumns")
#renameColumns  = dbutils.widgets.get("RenameColumns")
#textToDateColumns  = dbutils.widgets.get("ToDateColumns")
#nullConversionColumns  = dbutils.widgets.get("NullConversionColumns")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Read Raw Zone

# CELL ********************

print(InputRawBlobFile)

InputRawBlobFileWithPath = createRawFileAndPath(InputRawBlobFile,Workspace,Raw_Lakehouse)

print(InputRawBlobFileWithPath)

df = readRawFile_Fabric(InputRawBlobFileWithPath)

sourceCount = df.count()
print("sourceCount={}".format(sourceCount)) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Drop Duplicates

# CELL ********************

if sourceCount > 0:
    dropDuplicate(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Transform - RenameColumns

# CELL ********************

if sourceCount > 0 and RenameColumns != "":
    transformRename(df,RenameColumns)

#display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Transform - ToDateColumns

# CELL ********************

if sourceCount > 0 and ToDateColumns != "":
    transformToDate(df,ToDateColumns)

#display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Transform - NullConversionColumns

# CELL ********************

if sourceCount > 0 and NullConversionColumns != "":
    transformNullConversion(df,NullConversionColumns)

#display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Audit Data Points

# CELL ********************

if sourceCount > 0:
    
    df= df.withColumn("ELT_RawFile",lit(InputRawBlobFile))\
        .withColumn("ELT_TrustedTimestamp",lit(datetime.datetime.now().astimezone(pytz.timezone(TimeZone)).strftime("%Y-%m-%d %H:%M:%S")))

#display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Write - Trusted Zone

# CELL ********************

if sourceCount > 0:
    #writeTrustedFile(df,OutputTrustedBlobFile,OutputTrustedFileFormat,OutputTrustedFileWriteMode,KeyColumns)
    writeTrustedFile_Fabric(df,Trusted_Lakehouse,TargetName,KeyColumns)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Return Values

# CELL ********************

#import json
#dbutils.notebook.exit(json.dumps({
#    "sourceCount": sourceCount
#}))

mssparkutils.notebook.exit(sourceCount)  

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
