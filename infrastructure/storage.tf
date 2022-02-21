resource "azurerm_storage_account" "fry-bot" {
  name                     = "frybot"
  resource_group_name      = azurerm_resource_group.fry-bot.name
  location                 = azurerm_resource_group.fry-bot.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_table" "wordle" {
  name                 = "wordle"
  storage_account_name = azurerm_storage_account.fry-bot.name
}

resource "azurerm_storage_table" "haiku" {
  name                 = "wordle"
  storage_account_name = azurerm_storage_account.fry-bot.name
}

resource "azurerm_role_assignment" "table-contributor" {
  scope                = azurerm_storage_account.fry-bot.id
  role_definition_name = "Storage Table Data Contributor"
  principal_id         = azurerm_user_assigned_identity.fry-bot.principal_id
}
