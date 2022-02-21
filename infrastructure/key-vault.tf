resource "azurerm_key_vault" "fry-bot" {
  name                        = "fry-bot"
  location                    = azurerm_resource_group.fry-bot.location
  resource_group_name         = azurerm_resource_group.fry-bot.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}

resource "azurerm_key_vault_access_policy" "fry-bot" {
  key_vault_id = azurerm_key_vault.fry-bot.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.fry-bot.client_id

  secret_permissions = [
    "Get",
  ]
}
