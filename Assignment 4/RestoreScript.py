import os
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.storage.blob import BlobServiceClient

# Authentication
credential = DefaultAzureCredential()
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
sql_client = SqlManagementClient(credential, subscription_id)

# Variables
resource_group = "rg-webapp"
server_name = "sqlserverwebapp"
database_name = "sqldb-webapp"
storage_account_name = "sqlbackupsstorage"
container_name = "backups"
backup_file_name = f"{database_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.bacpac"

# Backup Process
backup_blob_uri = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{backup_file_name}"
sql_client.databases.begin_export(
    resource_group_name=resource_group,
    server_name=server_name,
    database_name=database_name,
    parameters={
        "storage_key_type": "StorageAccessKey",
        "storage_uri": backup_blob_uri,
        "administrator_login": os.getenv('AZURE_SQL_ADMIN'),
        "administrator_login_password": os.getenv('AZURE_SQL_PASSWORD')
    }
)

# Restore Process
def restore_database(backup_file_uri, new_database_name):
    sql_client.databases.begin_import(
        resource_group_name=resource_group,
        server_name=server_name,
        database_name=new_database_name,
        parameters={
            "storage_key_type": "StorageAccessKey",
            "storage_uri": backup_file_uri,
            "administrator_login": os.getenv('AZURE_SQL_ADMIN'),
            "administrator_login_password": os.getenv('AZURE_SQL_PASSWORD')
        }
    )

# List Backups
blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=credential)
container_client = blob_service_client.get_container_client(container_name)
blobs = container_client.list_blobs()
for blob in blobs:
    print(f"Name: {blob.name}, Last Modified: {blob.last_modified}")
