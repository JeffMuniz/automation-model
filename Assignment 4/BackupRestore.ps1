# Variables
$ResourceGroupName = "rg-webapp"
$ServerName = "sqlserverwebapp"
$DatabaseName = "sqldb-webapp"
$StorageAccountName = "sqlbackupsstorage"
$ContainerName = "backups"
$BackupFileName = "$DatabaseName-$(Get-Date -Format yyyyMMddHHmmss).bacpac"

# Backup Process
Export-AzSqlDatabase -ResourceGroupName $ResourceGroupName -ServerName $ServerName -DatabaseName $DatabaseName -StorageAccountName $StorageAccountName -StorageContainerName $ContainerName -StorageKeyType "StorageAccessKey" -FileName $BackupFileName

# Restore Process
function Restore-Database {
    param(
        [string]$BackupFile,
        [string]$NewDatabaseName
    )

    Import-AzSqlDatabase -ResourceGroupName $ResourceGroupName -ServerName $ServerName -DatabaseName $NewDatabaseName -StorageAccountName $StorageAccountName -StorageContainerName $ContainerName -StorageKeyType "StorageAccessKey" -FileName $BackupFile
}

# List Backups
$blobs = Get-AzStorageBlob -Container $ContainerName -Context (Get-AzStorageAccount -ResourceGroupName $ResourceGroupName -Name $StorageAccountName).Context
$blobs | Select Name, LastModified


