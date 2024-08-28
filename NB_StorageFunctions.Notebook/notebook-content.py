# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

%run NB_KeyVaultFunctions

# MARKDOWN ********************

# getRawFile Function

# CELL ********************

def getRawFile(file=None):
  # ##########################################################################################################################  
  # Function: getRawFile
  # Returns a fully qualified name of a file in Raw Zone of Azure Blob Storage
  # 
  # Parameters:
  # file = file name including extension
  # 
  # Returns:
  # The fully qualified name of a file in Raw Zone of Azure Blob Storage
  # ##########################################################################################################################  
  storageAccountName = getSecret("adls-accountname")
  storageAccountKey = getSecret("adls-accesskey")
  spark.conf.set("fs.azure.account.key." + storageAccountName + ".blob.core.windows.net", storageAccountKey)
  
  rawFile ="wasbs://raw@"+ storageAccountName + ".blob.core.windows.net/" + file
  
  return rawFile

# MARKDOWN ********************

# getTrustedFile Function

# CELL ********************

def getTrustedFile(file=None):
  # ##########################################################################################################################  
  # Function: getTrustedFile
  # Returns a fully qualified name of a file in Trusted Zone of Azure Blob Storage
  # 
  # Parameters:
  # file = file name including extension
  # 
  # Returns:
  # The fully qualified name of a file in Trusted Zone of Azure Blob Storage
  # ##########################################################################################################################    
  storageAccountName = getSecret("adls-accountname")
  storageAccountKey = getSecret("adls-accesskey")
  spark.conf.set("fs.azure.account.key." + storageAccountName + ".blob.core.windows.net", storageAccountKey)
  
  trustedFile ="wasbs://trusted@"+ storageAccountName + ".blob.core.windows.net/" + file
  
  return trustedFile

# MARKDOWN ********************

# getCuratedFile Function

# CELL ********************

def getCuratedFile(file=None):
  # ##########################################################################################################################  
  # Function: getCuratedFile
  # Returns a fully qualified name of a file in Curated Zone of Azure Blob Storage
  # 
  # Parameters:
  # file = file name including extension
  # 
  # Returns:
  # The fully qualified name of a file in Curated Zone of Azure Blob Storage
  # ##########################################################################################################################    
  storageAccountName = getSecret("adls-accountname")
  storageAccountKey = getSecret("adls-accesskey")
  spark.conf.set("fs.azure.account.key." + storageAccountName + ".blob.core.windows.net", storageAccountKey)
  
  curatedFile ="wasbs://curated@"+ storageAccountName + ".blob.core.windows.net/" + file
  
  return curatedFile

# MARKDOWN ********************

# create full path for Raw file

# CELL ********************

def createRawFileAndPath(file=None,workspace=None,lakehouse=None):

    filewithpath = "abfss://"+workspace+"@onelake.dfs.fabric.microsoft.com/"+lakehouse+".Lakehouse/"+file
    return filewithpath

# MARKDOWN ********************

# readRawFile Function

# CELL ********************

def readRawFile_Fabric(file=None):
  # ##########################################################################################################################  
  # Function: readRawFile
  # Reads a file from Raw Data Lake and returns as dataframe
  # 
  # Parameters:
  # file = file name including extension
  # 
  # Returns:
  # A dataframe of the raw file
  # ##########################################################################################################################    

  #df = spark.read.parquet(file)
  
  fabricFile = file
  if ".csv" in fabricFile:
    df = spark.read.csv(path=fabricFile, sep=",", header="true", inferSchema="true")
  elif ".parquet" in fabricFile:
    df = spark.read.parquet(fabricFile)
  else:
    df = spark.read.format("csv").load(fabricFile)

  return df


def readRawFile(file=None):
  # ##########################################################################################################################  
  # Function: readRawFile
  # Reads a file from raw zone of Azure Blob Storage and returns as dataframe
  # 
  # Parameters:
  # file = file name including extension
  # 
  # Returns:
  # A dataframe of the raw file
  # ##########################################################################################################################    
  rawFile = getRawFile(file)
  if ".csv" in rawFile:
    df = spark.read.csv(path=rawFile, sep=",", header="true", inferSchema="true")
  elif ".parquet" in rawFile:
    df = spark.read.parquet(rawFile)
  elif ".orc" in rawFile:
    df = spark.read.orc(rawFile)
  elif ".json" in rawFile:
    df = spark.read.json(rawFile)
  else:
    df = spark.read.format("csv").load(rawFile)
    
  return df

# MARKDOWN ********************

# readTrustedFile Function

# CELL ********************

def readTrustedFile(file=None, fileFormat=None):
  # ##########################################################################################################################  
  # Function: readC1File
  # Reads a file from trusted zone of Azure Blob Storage and returns as dataframe
  # 
  # Parameters:
  # file = file name including extension
  # fileFormat = file format
  # 
  # Returns:
  # A dataframe of the trusted file
  # ##########################################################################################################################    
  trustedFile = getTrustedFile(file)
  if "csv" in fileFormat:
    df = spark.read.csv(path=trustedFile, sep=",", header="true", inferSchema="true")
  elif "parquet" in fileFormat:
    df = spark.read.parquet(trustedFile)
  elif "orc" in fileFormat:
    df = spark.read.orc(trustedFile)
  elif "json" in fileFormat:
    df = spark.read.json(path=trustedFile,multiLine="true")
  elif "delta" in fileFormat:
    df = spark.read.format("delta").load(trustedFile)
  else:
    df = spark.read.format("csv").load(trustedFile)
    
  return df

# MARKDOWN ********************

# readCuratedFile Function

# CELL ********************

def readCuratedFile(file=None, fileFormat=None):
  # ##########################################################################################################################  
  # Function: readCuratedFile
  # Reads a file from curated zone of Azure Blob Storage and returns as dataframe
  # 
  # Parameters:
  # file = file name including extension
  # fileFormat = file format
  # 
  # Returns:
  # A dataframe of the curated file
  # ##########################################################################################################################    
  curatedFile = getCuratedFile(file)
  if "csv" in fileFormat:
    df = spark.read.csv(path=curatedFile, sep=",", header="true", inferSchema="true")
  elif "parquet" in fileFormat:
    df = spark.read.parquet(curatedFile)
  elif "orc" in fileFormat:
    df = spark.read.orc(curatedFile)
  elif "json" in fileFormat:
    df = spark.read.json(path=curatedFile,multiLine="true")
  elif "delta" in fileFormat:
    df = spark.read.format("delta").load(curatedFile)
  else:
    df = spark.read.format("csv").load(curatedFile)
    
  return df

# MARKDOWN ********************

# readSqlDbTable Function

# CELL ********************

def readSqlDbTable(sqlTable=None):
  # ##########################################################################################################################  
  # Function: readSqlDbTable
  # Reads Table from Sql Database Connection
  # 
  # Parameters:
  # sqlTable = Sql Database TableName
  # 
  # Returns:
  # A dataframe of the Sql Database Table
  # ##########################################################################################################################    
  sqlDbConnectionString = getSecret("EDW-jdbc-connectionstring")
  df = spark.read.jdbc(url=sqlDbConnectionString, table = sqlTable)
  
  return df

# MARKDOWN ********************

# writeTrustedFile Function

# CELL ********************

def writeTrustedFile_Fabric(df, OutputDatabase=None, OutputTable=None, keyColumns=None):
  # ##########################################################################################################################  
  # Function: writeTrustedFile_Fabric
  # Writes the input dataframe to a file in trusted zone of Azure Blob
  # 
  # Parameters:
  # df = input dataframe
  # file = file name including extension
  # fileFormat = File format. Supported formats are csv/parquet/orc/json/delta
  # writeMode = mode of writing the trusted file. Allowed values - upsert/append/overwrite/ignore/error/errorifexists
  # keyColumns = key columns
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  Destination = OutputDatabase + "." + OutputTable
  
  df.write.mode("overwrite").format("delta").saveAsTable(Destination)

  return

# CELL ********************

def writeTrustedFile(df, file=None, fileFormat=None, writeMode=None, keyColumns=None):
  # ##########################################################################################################################  
  # Function: writeTrustedFile
  # Writes the input dataframe to a file in trusted zone of Azure Blob
  # 
  # Parameters:
  # df = input dataframe
  # file = file name including extension
  # fileFormat = File format. Supported formats are csv/parquet/orc/json/delta
  # writeMode = mode of writing the trusted file. Allowed values - upsert/append/overwrite/ignore/error/errorifexists
  # keyColumns = key columns
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  trustedFile= getTrustedFile(file)
  if "csv" in fileFormat:
    df.write.csv(trustedFile,mode=writeMode,sep=",",header="true", timestampFormat ="yyyy-MM-dd HH:mm:ss")
  elif "parquet" in fileFormat:
    df.write.parquet(trustedFile,mode=writeMode)
  elif "orc" in fileFormat:
    df.write.orc(trustedFile,mode=writeMode)
  elif "json" in fileFormat:
    df.write.json(trustedFile, mode=writeMode)
  elif "delta" in fileFormat:
    if "upsert" in writeMode:
      if DeltaTable.isDeltaTable(spark,trustedFile):
        upsertDeltaLakeData(trustedFile, df, keyColumns)
      else:
        df.write.format("delta").save(trustedFile)
    elif "delete-insert" in writeMode:
      if DeltaTable.isDeltaTable(spark,trustedFile):
        deleteInsertDeltaLakeData(trustedFile, df, keyColumns)
      else:
        df.write.format("delta").save(trustedFile)
    else:
      df.write.option("overwriteSchema","true").format("delta").mode(writeMode).save(trustedFile)
  else:
    df.write.save(path=trustedFile,format=fileFormat,mode=writeMode)
  return

# MARKDOWN ********************

# writeCuratedFile Function

# CELL ********************

def writeCuratedFile(df, file=None, fileFormat=None, writeMode=None, keyColumns=None):
  # ##########################################################################################################################  
  # Function: writeCuratedFile
  # Writes the input dataframe to a file in curated zone of Azure Blob
  # 
  # Parameters:
  # df = input dataframe
  # file = full file name including extension
  # fileFormat = File format. Supported formats are csv/parquet/orc/json/delta
  # writeMode = mode of writing the trusted file. Allowed values - upsert/append/overwrite/ignore/error/errorifexists
  # keyColumns = key columns
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  curatedFile= getCuratedFile(file)
  if "csv" in fileFormat:
    df.write.csv(curatedFile,mode=writeMode,sep=",",header="true", timestampFormat ="yyyy-MM-dd HH:mm:ss")
  elif "parquet" in fileFormat:
    df.write.parquet(curatedFile,mode=writeMode)
  elif "orc" in fileFormat:
    df.write.orc(curatedFile,mode=writeMode)
  elif "json" in fileFormat:
    df.write.json(curatedFile, mode=writeMode)
  elif "delta" in fileFormat:
    if "upsert" in writeMode:
      if DeltaTable.isDeltaTable(spark,curatedFile):
        upsertDeltaLakeData(curatedFile, df, keyColumns)
      else:
        df.write.format("delta").save(curatedFile)
    elif "delete-insert" in writeMode:
      if DeltaTable.isDeltaTable(spark,curatedFile):
        deleteInsertDeltaLakeData(curatedFile, df, keyColumns)
      else:
        df.write.format("delta").save(curatedFile)
    else:
      df.write.option("overwriteSchema","true").format("delta").mode(writeMode).save(curatedFile)
  else:
    df.write.save(path=curatedFile,format=fileFormat,mode=writeMode)
  return

# MARKDOWN ********************

# upsertDeltaLakeData Function

# CELL ********************

def upsertDeltaLakeData(deltaLakePath, df, keyColumns):
  # ##########################################################################################################################  
  # Function: upsertDeltaLakeData
  # Upserts data into Delta Lake Table
  # 
  # Parameters:
  # deltaLakePath = DeltaLake file path on Azure Data Lake Storage Gen2
  # df = new dataframe
  # 
  # Returns:
  # NULL
  # ########################################################################################################################## 
  
  keyColumnList = keyColumns.split(",")
  joinCondition = ""
    
  for keyColumn in keyColumnList:
    joinCondition = joinCondition + "new."+keyColumn+" = old."+keyColumn + " and "
  
  joinCondition = joinCondition[0:len(joinCondition) - 5]
  
  deltaTable = DeltaTable.forPath(spark, deltaLakePath)
  
  deltaTable.alias("old").merge(
      df.alias("new"), 
      joinCondition) \
  .whenMatchedUpdateAll() \
  .whenNotMatchedInsertAll() \
  .execute()

# MARKDOWN ********************

# deleteInsertDeltaLakeData Function

# CELL ********************

def upsertDeltaLakeData(deltaLakePath, df, keyColumns):
  # ##########################################################################################################################  
  # Function: upsertDeltaLakeData
  # Upserts data into Delta Lake Table
  # 
  # Parameters:
  # deltaLakePath = DeltaLake file path on Azure Data Lake Storage Gen2
  # df = new dataframe
  # 
  # Returns:
  # NULL
  # ########################################################################################################################## 
  
  keyColumnList = keyColumns.split(",")
  joinCondition = ""
    
  for keyColumn in keyColumnList:
    joinCondition = joinCondition + "new."+keyColumn+" = old."+keyColumn + " and "
  
  joinCondition = joinCondition[0:len(joinCondition) - 5]
  
  deltaTable = DeltaTable.forPath(spark, deltaLakePath)
  
  deltaTable.alias("old").merge(
      df.alias("new"), 
      joinCondition) \
  .whenMatchedUpdateAll() \
  .whenNotMatchedInsertAll() \
  .execute()

# MARKDOWN ********************

# deleteInsertDeltaLakeData Function

# CELL ********************

def deleteInsertDeltaLakeData (deltaLakePath, df, keyColumns):
  # ##########################################################################################################################  
  # Function: deleteInsertDeltaLakeData 
  # Delete and Insert data into Delta Lake Table
  # 
  # Parameters:
  # deltaLakePath = DeltaLake file path on Azure Data Lake Storage Gen2
  # df = new dataframe
  # 
  # Returns:
  # NULL
  # ########################################################################################################################## 
  
  keyColumnList = keyColumns.split(",")
  joinCondition = ""
    
  for keyColumn in keyColumnList:
    joinCondition = joinCondition + "new."+keyColumn+" = old."+keyColumn + " and "
  
  joinCondition = joinCondition[0:len(joinCondition) - 5]
  
  deltaTable = DeltaTable.forPath(spark, deltaLakePath)
  
  deltaTable.alias("old").merge(
      df.alias("new"), 
      joinCondition) \
  .whenMatchedDeleteAll() \
  .whenNotMatchedInsertAll() \
  .execute()

# MARKDOWN ********************

# writeStgTable Function

# CELL ********************

def writeStgTable(df, sqlSchema=None, sqlTable=None):
  # ##########################################################################################################################  
  # Function: writeStgTable
  # Writes the input dataframe to a stg table in EDW
  # 
  # Parameters:
  # df = input dataframe
  # sqlSchema = table schema
  # sqlTable = table name
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  EDWConnectionString = getSecret("EDW-jdbc-connectionstring")
     
  if "azuresynapse" in EDWConnectionString:
    writeStgTableSynapse(df,sqlSchema,sqlTable)
  else:
    writeStgTableSQL(df,sqlSchema,sqlTable)    
  
  return

# MARKDOWN ********************

# writeStgTableSQL Function

# CELL ********************

def writeStgTableSQL (df, sqlSchema=None, sqlTable=None):
  # ##########################################################################################################################  
  # Function: writeStgTable
  # Writes the input dataframe to a stg table in EDW
  # 
  # Parameters:
  # df = input dataframe
  # sqlSchema = table schema
  # sqlTable = table name
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  EDWConnectionString = getSecret("EDW-jdbc-connectionstring")
  sqlTableName = "stg." + sqlSchema + "_" + sqlTable
  df.write.option("truncate", "true").jdbc(url=EDWConnectionString, table=sqlTableName, mode="overwrite")
  return

# MARKDOWN ********************

# executeSqlOnEDW function

# CELL ********************

def executeSqlOnEDW(sql=None):
  # ##########################################################################################################################  
  # Function: executeSqlOnEDW_JDBC
  # run sql statements on EDW Database using built-in java JDBC-driver
  # 
  # Parameters:
  # sql = sql statement
  # 
  # Returns:
  # 
  # ########################################################################################################################## 
  sqlDbConnectionString = getSecret("EDW-jdbc-connectionstring")
  password = getSecret("synapse-password")
      
  # Fetch the driver manager from your spark context
  driver_manager = spark._sc._gateway.jvm.java.sql.DriverManager
    
  # Create a connection object using a jdbc-url, + sql uname & pass
  con = driver_manager.getConnection(sqlDbConnectionString, "synapseadmin", password)

  # Create callable statement and execute it
  exec_statement = con.prepareCall(sql)
  exec_statement.execute()

  # Close connections
  exec_statement.close()
  return

# MARKDOWN ********************

# Get Max Timestamp

# CELL ********************

def getMaxTimestamp(sqlTable=None):
  sqlDbConnectionString = getSecret("EDW-jdbc-connectionstring")

  MaxCol = "ELT_TrustedTimestamp"

  query = "(SELECT isnull(MAX({col}),'1900-01-01') MaxTimestamp FROM {Table}) T".format(Table=sqlTable, col=MaxCol)

  df = spark.read.jdbc(url=sqlDbConnectionString, table = query)
  
  return df

# CELL ********************

def SynapseGetBlobStorageStageFolder():
  BLOB_ACCESS_KEY = getSecret("adls-accesskey")

  BLOB_CONTAINER = "synapsestaging"
  ADS_DATA_LAKE_ACCOUNT = getSecret("adls-accountname")

  TEMPFOLDER = "abfss://" + BLOB_CONTAINER + "@" + ADS_DATA_LAKE_ACCOUNT + ".dfs.core.windows.net" + "/temp"

  # Set up the Blob Storage account access key in the notebook session conf.
  spark.conf.set("fs.azure.account.key." +  ADS_DATA_LAKE_ACCOUNT + ".dfs.core.windows.net" + "", BLOB_ACCESS_KEY)
  spark.conf.set("spark.sql.parquet.writeLegacyFormat", "true")
  
  sc._jsc.hadoopConfiguration().set("fs.azure.account.key." +  ADS_DATA_LAKE_ACCOUNT + ".dfs.core.windows.net" + "", BLOB_ACCESS_KEY)
  
  return TEMPFOLDER

# CELL ********************

def writeStgTableSynapse(dataframe, sqlSchema, sqlTable):
  
  SQL_DW_URL = getSecret("EDW-jdbc-connectionstring")
  TEMPFOLDER = SynapseGetBlobStorageStageFolder()
  
  sqlTableName = "stg." + sqlSchema + "_" + sqlTable
  
  print(TEMPFOLDER)
  print(SQL_DW_URL)
  
  #print("Writing data to table " + tablename + " with mode " + writemode)
  
  dataframe.write \
  .format("com.databricks.spark.sqldw") \
  .option("url", SQL_DW_URL) \
  .option("useAzureMSI", "true") \
  .option("dbtable", sqlTableName) \
  .option("tempdir", TEMPFOLDER) \
  .mode("overwrite") \
  .save()
