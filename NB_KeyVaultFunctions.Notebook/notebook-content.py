# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# listSecrets Function

# CELL ********************

def listSecrets():
# ##########################################################################################################################  
# Function: listSecrets
# Returns all secrets stored in Azure Key Vault. Uses Azure Key Vault backed scope
# 
# Parameters:
# None
# 
# Returns:
# A list of all secrets stored in Azure Key Vault.
# ##########################################################################################################################
  kvscope="dbw-secretscope"
  return dbutils.secrets.list(kvscope)

# MARKDOWN ********************

# getSecret Function

# CELL ********************

def getSecret(secretName):
# ##########################################################################################################################  
# Function: getSecret
# Returns the value of a secret stored in Azure Key Vault. Uses Azure Key Vault backed scope
# 
# Parameters:
# secretName = Name of secret in Azure Key Vault
# 
# Returns:
# The value of secret stored in Azure Key Vault
# ##########################################################################################################################
  kvScope="dbw-secretscope"
  secretValue = dbutils.secrets.get(kvScope,secretName)
  return secretValue
