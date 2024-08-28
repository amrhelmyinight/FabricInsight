# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

import uuid

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.window import *
from delta.tables import *
import datetime

import pytz

# MARKDOWN ********************

# dropDuplicate Function

# CELL ********************

def dropDuplicate(df):
  # ##########################################################################################################################  
  # Function: dropDuplicate
  # converts De Duplicates records in Dataframe
  # 
  # Parameters:
  # df = dataframe
  # 
  # Returns:
  # dataframe
  # ########################################################################################################################## 
  
  df = df.dropDuplicates()

  return df

# MARKDOWN ********************

# transformRename Function

# CELL ********************

def transformRename(df,columns=None):
  # ##########################################################################################################################  
  # Function: transformRename
  # rename columns
  # 
  # Parameters:
  # df = dataframe
  # columns = list of columns to be renamed
  # 
  # Returns:
  # dataframe
  # ########################################################################################################################## 
  
  columnList = columns.split(",")

  for columnName in columnList:
        oldName = columnName[0:columnName.find('|')]
        newName = columnName[columnName.find('|')+1:]
        df = df.withColumnRenamed(oldName,newName)
    
  return df
  

# MARKDOWN ********************

# transformToDate Function

# CELL ********************

def transformToDate(df,columns=None):
  # ##########################################################################################################################  
  # Function: transformToDate
  # converts columns to date type yyyy-MM-dd
  # 
  # Parameters:
  # df = dataframe
  # columns = list of columns for Date Conversion
  # 
  # Returns:
  # dataframe
  # ########################################################################################################################## 
  
  columnList = columns.split(",")

  for columnName in columnList:
        df = df.withColumn(columnName, to_date(col(columnName),"yyyy-MM-dd"))

  return df
  

# MARKDOWN ********************

# transformNullConversion Function

# CELL ********************

def transformNullConversion(df,columns=None):
  # ##########################################################################################################################  
  # Function: transformNullConversion
  # converts Null values in int type columns to 0
  # 
  # Parameters:
  # df = dataframe
  # columns = list of columns for Null Conversion
  # 
  # Returns:
  # dataframe
  # ########################################################################################################################## 
  
  columnList = columns.split(",")

  for columnName in columnList:
        df = df.na.fill(value=0,subset=[columnName])

  return df
