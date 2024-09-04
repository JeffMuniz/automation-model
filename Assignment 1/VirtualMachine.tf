resource "azurerm_network_interface" "web_nic" {
  count               = 2
  name                = "webnic-${count.index}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.web.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "web_vm" {
  count               = 2
  name                = "webvm-${count.index}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  size                = "Standard_DS1_v2"
  admin_username      = "adminuser"
  admin_password      = "P@ssw0rd1234"

  network_interface_ids = [
    azurerm_network_interface.web_nic[count.index].id,
  ]

  os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}

resource "azurerm_lb" "web_lb" {
  name                = "web-lb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
}

resource "azurerm_lb_backend_address_pool" "bpepool" {
  name                = "beapool"
  resource_group_name = azurerm_resource_group.rg.name
  loadbalancer_id     = azurerm_lb.web_lb.id
}

resource "azurerm_lb_rule" "lbrule" {
  name                            = "http"
  resource_group_name             = azurerm_resource_group.rg.name
  loadbalancer_id                 = azurerm_lb.web_lb.id
  frontend_ip_configuration_name  = azurerm_lb.web_lb.frontend_ip_configuration[0].name
  backend_address_pool_id         = azurerm_lb_backend_address_pool.bpepool.id
  protocol                        = "Tcp"
  frontend_port                   = 80
  backend_port                    = 80
}
