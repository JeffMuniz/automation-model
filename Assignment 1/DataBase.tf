resource "azurerm_sql_server" "sql_server" {
  name                         = "sqlserverwebapp"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "P@ssw0rd1234"
}

resource "azurerm_sql_database" "sql_db" {
  name                = "sqldb-webapp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql_server.name
  edition             = "Standard"
  requested_service_objective_name = "S1"
}
