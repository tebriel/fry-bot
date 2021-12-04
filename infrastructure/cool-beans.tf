resource "azurerm_storage_account" "cool-beans" {
  name                     = "massbotcoolbeans"
  resource_group_name      = azurerm_resource_group.fry-bot.name
  location                 = azurerm_resource_group.fry-bot.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "cool-beans" {
  name                  = "cool-beans"
  storage_account_name  = azurerm_storage_account.cool-beans.name
  container_access_type = "private"
}