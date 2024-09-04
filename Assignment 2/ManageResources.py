import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, Kind
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, filename='azure_resources.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize clients
credential = DefaultAzureCredential()
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
sql_client = SqlManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

# Variables
resource_group_name = "myResourceGroup"
location = "eastus"

# 1. Create Resource Group
def create_resource_group():
    try:
        rg_result = resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})
        logging.info(f"Resource group {resource_group_name} created/updated in {location}.")
        return rg_result
    except Exception as e:
        logging.error(f"Error creating resource group: {e}")

# 2. Deploy a Virtual Machine
def create_virtual_machine():
    try:
        # Simplified example, you would need to specify more details here.
        vm_result = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name,
            "myVM",
            {
                "location": location,
                "storage_profile": {
                    "image_reference": {
                        "publisher": "Canonical",
                        "offer": "UbuntuServer",
                        "sku": "18.04-LTS",
                        "version": "latest"
                    }
                },
                "hardware_profile": {
                    "vm_size": "Standard_B1ls"
                },
                "os_profile": {
                    "computer_name": "myVM",
                    "admin_username": "azureuser",
                    "admin_password": "YourPassword1234"
                },
                "network_profile": {
                    "network_interfaces": [{
                        "id": "/subscriptions/<subscription-id>/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/<nic-name>",
                    }]
                }
            }
        )
        vm_result.result()  # Wait for VM creation to complete
        logging.info(f"VM 'myVM' created in resource group {resource_group_name}.")
    except Exception as e:
        logging.error(f"Error creating VM: {e}")

# 3. Set up Azure SQL Database
def create_sql_database():
    try:
        # Create SQL Server and Database
        sql_server = sql_client.servers.begin_create_or_update(
            resource_group_name,
            "mySqlServer",
            {
                "location": location,
                "version": "12.0",
                "administrator_login": "sqladmin",
                "administrator_login_password": "YourPassword1234"
            }
        )
        sql_server.result()
        sql_db = sql_client.databases.begin_create_or_update(
            resource_group_name,
            "mySqlServer",
            "myDatabase",
            {
                "location": location,
                "sku": {"name": "S0", "tier": "Standard"}
            }
        )
        sql_db.result()
        logging.info(f"SQL Database 'myDatabase' created in resource group {resource_group_name}.")
    except Exception as e:
        logging.error(f"Error creating SQL Database: {e}")

# 4. Configure Storage Account
def create_storage_account():
    try:
        storage_account_params = StorageAccountCreateParameters(
            sku=Sku(name="Standard_LRS"),
            kind=Kind.STORAGE_V2,
            location=location
        )
        storage_account = storage_client.storage_accounts.begin_create(
            resource_group_name,
            "mystorageaccount",
            storage_account_params
        )
        storage_account.result()
        logging.info(f"Storage Account 'mystorageaccount' created in resource group {resource_group_name}.")
    except Exception as e:
        logging.error(f"Error creating Storage Account: {e}")

# Utility Functions: Start, Stop, Delete VM
def start_vm():
    try:
        start_result = compute_client.virtual_machines.begin_start(resource_group_name, "myVM")
        start_result.result()
        logging.info(f"VM 'myVM' started.")
    except Exception as e:
        logging.error(f"Error starting VM: {e}")

def stop_vm():
    try:
        stop_result = compute_client.virtual_machines.begin_deallocate(resource_group_name, "myVM")
        stop_result.result()
        logging.info(f"VM 'myVM' stopped.")
    except Exception as e:
        logging.error(f"Error stopping VM: {e}")

def delete_vm():
    try:
        delete_result = compute_client.virtual_machines.begin_delete(resource_group_name, "myVM")
        delete_result.result()
        logging.info(f"VM 'myVM' deleted.")
    except Exception as e:
        logging.error(f"Error deleting VM: {e}")

# Main execution
if __name__ == "__main__":
    create_resource_group()
    create_virtual_machine()
    create_sql_database()
    create_storage_account()
