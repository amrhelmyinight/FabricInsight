# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # 📌 Attach Default Lakehouse
# ❗**Note the code in the cell that follows is required to programatically attach the lakehouse and enable the running of spark.sql(). If this cell fails simply restart your session as this cell MUST be the first command executed on session start.**

# CELL ********************

# MAGIC %%configure
# MAGIC {
# MAGIC     "defaultLakehouse": {  
# MAGIC         "name": "lh_fa_raw",
# MAGIC     }
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
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
from datetime import datetime
import os
import json
import requests
import base64
import time

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # #️⃣ Functions

# CELL ********************


def get_file_content_using_notebookutils(file):
    """Get the content of a file using notebookutils."""
    #return self.mssparkutils.fs.head(file, 1000000000)
    data = spark.sparkContext.wholeTextFiles(file).collect() # type: ignore

    # data is a list of tuples, where the first element is the file path and the second element is the content of the file
    file_content = data[0][1]

    return file_content


def update_notebook(ntbk_name, ntbk_json, workspace_id, ntbk_id):

        api_endpoint = "api.fabric.microsoft.com"
        pbi_token = mssparkutils.credentials.getToken('https://analysis.windows.net/powerbi/api') 

        print(f"Updating '{ntbk_name}'...")
        url = f"https://{api_endpoint}/v1/workspaces/{workspace_id}/items/{ntbk_id}/updateDefinition"

        json_str = json.dumps(ntbk_json)
        json_bytes = json_str.encode('utf-8')
        base64_encoded_json = base64.b64encode(json_bytes)
        base64_str = base64_encoded_json.decode('utf-8')
        print('payload')
        payload = json.dumps({
            "definition" : {
                "format": "ipynb",
                "parts" : [
                    {
                        "path": "notebook-content.ipynb",
                        "payload": base64_str,
                        "payloadType": "InlineBase64"
                    }
                ]
            }
        })

        headers = {
            'Authorization': f'Bearer {pbi_token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.ok:
            print(f">> Notebook '{ntbk_name}' updated.")
        else:
            raise RuntimeError(f"Notebook '{ntbk_name}' update failed: {response.status_code}: {response.text}")


def import_notebooks(output_folder, workspace_id, notebook_names=None):
        date = datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
        resource_type = "notebooks"
        res_imported = 0
        resources_imported = {}
        existing_nb_id = None
        artifact_path = f"{output_folder}"

        if not mssparkutils.fs.exists(artifact_path):
            print(f"Path where the import artifacts from Synapse are located {artifact_path} does not exist. Exiting ...")
            return

        print(f"Importing individual resources of type '{resource_type}' into Fabric workspace '{workspace_id}'...")
        notebook_names_raw = [f.name for f in mssparkutils.fs.ls(artifact_path)]
        notebook_names = [name.replace('.ipynb','') for name in notebook_names_raw if name.endswith(".ipynb")]
        print(notebook_names)
        existing_nbs = get_notebooks(workspace_id)

        for notebook_name in notebook_names:
            time.sleep(2)
            existing_nb = [nb for nb in existing_nbs if nb['displayName'] == notebook_name ]
            if len(existing_nb) == 1:
                print(f'{notebook_name} exists already... updating...')
                existing_nb_id = existing_nb[0]['id'] 
            
            file_path = os.path.join(artifact_path, f"{notebook_name}.ipynb")
            if mssparkutils.fs.exists(file_path):
                read_file = get_file_content_using_notebookutils(file_path)
                ntbk_json = json.loads(read_file)
                ntbk_name = f"{notebook_name}"
                if existing_nb_id == None:
                    import_notebook(ntbk_name, ntbk_json, workspace_id, False)
                else:
                    update_notebook(ntbk_name, ntbk_json, workspace_id, existing_nb_id)
                res_imported += 1

        resources_imported[resource_type] = res_imported
        print(f"Finish importing {res_imported} items of type: {resource_type}")

def import_notebook(ntbk_name, ntbk_json, workspace_id, overwrite=False):

    api_endpoint = "api.fabric.microsoft.com"
    pbi_token = mssparkutils.credentials.getToken('https://analysis.windows.net/powerbi/api') 

    print(f"Importing '{ntbk_name}'...")
    url = f"https://{api_endpoint}/v1/workspaces/{workspace_id}/items"

    json_str = json.dumps(ntbk_json)
    json_bytes = json_str.encode('utf-8')
    base64_encoded_json = base64.b64encode(json_bytes)
    base64_str = base64_encoded_json.decode('utf-8')

    payload = json.dumps({
        "type": "Notebook",
        "description": "Imported from Synapse",
        "displayName": ntbk_name,
        "definition" : {
            "format": "ipynb",
            "parts" : [
                {
                    "path": "notebook-content.ipynb",
                    "payload": base64_str,
                    "payloadType": "InlineBase64"
                }
            ]
        }
    })

    headers = {
        'Authorization': f'Bearer {pbi_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:
        print(f">> Notebook '{ntbk_name}' created.")
    else:
        raise RuntimeError(f"Notebook '{ntbk_name}' creation failed: {response.status_code}: {response.text}")


def get_notebooks(workspace_id):
    api_endpoint = "api.fabric.microsoft.com"
    pbi_token = mssparkutils.credentials.getToken('https://analysis.windows.net/powerbi/api') 

    url = f"https://{api_endpoint}/v1/workspaces/{workspace_id}/items?type=Notebook"

    headers = {
        'Authorization': f'Bearer {pbi_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    if response.ok:        
        nbs = []
        for rr in response.json()['value']:
            nb = {}
            nb['id'] = rr['id'] 
            nb['displayName'] = rr['displayName']
            nb['matched'] = False
            nbs.append(nb)
        return nbs
    else:
        raise RuntimeError(f"Notebook '{ntbk_name}' creation failed: {response.status_code}: {response.text}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Run Import

# CELL ********************


import_notebooks(f"abfss://ece02e6c-3fca-4522-b360-fb40feb0b364@onelake.dfs.fabric.microsoft.com/7556b01a-56d8-4390-9f32-f5f80ff0ec90/Files/notebooks", "ece02e6c-3fca-4522-b360-fb40feb0b364")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
