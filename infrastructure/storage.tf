resource "azurerm_storage_account" "fry-bot" {
  name                     = "frybot"
  resource_group_name      = azurerm_resource_group.fry-bot.name
  location                 = azurerm_resource_group.fry-bot.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "haiku" {
  name                  = "haiku"
  storage_account_name  = azurerm_storage_account.fry-bot.name
  container_access_type = "private"
}

resource "azurerm_storage_table" "wordle" {
  name                 = "wordle"
  storage_account_name = azurerm_storage_account.fry-bot.name
}
