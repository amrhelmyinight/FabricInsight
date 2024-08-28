# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "bdb0971d-b86c-40cb-ba0a-449a15534605",
# META       "default_lakehouse_name": "lh_Viva_Raw",
# META       "default_lakehouse_workspace_id": "ece02e6c-3fca-4522-b360-fb40feb0b364"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
import zipfile
import io
import pyspark.sql.functions as F

# Replace with your API endpoint, bearer token, and lakehouse destination
api_endpoint = "https://www.yammer.com/api/v1/export?since=2024-08-09T00:00:00+00:00&model=User"
bearer_token = "255531-j382lj4gHwUAvKwpSQWXg"
lakehouse_destination = "/lakehouse/default/Files/Viva_User"

# Make the API request with Bearer authentication
headers = {"Authorization": f"Bearer {bearer_token}"}
response = requests.get(api_endpoint, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Create a temporary directory to store the downloaded ZIP file
    
    z = zipfile.ZipFile(io.BytesIO(response.content))
    # Create a SparkSession
    z.extractall(lakehouse_destination)

else:
    print("Error downloading files:", response.status_code)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
import zipfile
import io
import pyspark.sql.functions as F

# Replace with your API endpoint, bearer token, and lakehouse destination
model = "User"
api_endpoint = f"https://www.yammer.com/api/v1/export?since=2024-08-09T00:00:00+00:00&model={model}&include=csv"
bearer_token = "255531-j382lj4gHwUAvKwpSQWXg"
lakehouse_destination = f"/lakehouse/default/Files/Viva_{model}"

# Make the API request with Bearer authentication
headers = {"Authorization": f"Bearer {bearer_token}"}
response = requests.get(api_endpoint, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Create a temporary directory to store the downloaded ZIP file
    
    z = zipfile.ZipFile(io.BytesIO(response.content))
    # Create a SparkSession
    z.extractall(lakehouse_destination)

else:
    print("Error downloading files:", response.status_code)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
import zipfile
import io
import pyspark.sql.functions as F

# Replace with your API endpoint, bearer token, and lakehouse destination
model = "User"
api_endpoint = f"https://www.yammer.com/api/v1/export?since=2024-08-09T00:00:00+00:00&model={model}&include=csv"
bearer_token = "255531-j382lj4gHwUAvKwpSQWXg"
lakehouse_destination = f"abfss://Fabric_PoC@onelake.dfs.fabric.microsoft.com/lh_Viva_Raw.Lakehouse/Files/Viva_{model}"

df = spark.read.option("header",True) \
            .csv(lakehouse_destination + "/Users.csv")
df.show()
df.write.mode("overwrite").saveAsTable("Users")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
