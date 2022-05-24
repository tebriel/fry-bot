resource "azurerm_log_analytics_workspace" "fry-bot" {
  name                       = "fry-bot"
  location                   = azurerm_resource_group.fry-bot.location
  resource_group_name        = azurerm_resource_group.fry-bot.name
  sku                        = "PerGB2018"
  retention_in_days          = 30
  daily_quota_gb             = 0.5
}

resource "github_actions_secret" "workspace-key" {
  repository      = "fry-bot"
  secret_name     = "WORKSPACE_KEY"
  plaintext_value = azurerm_log_analytics_workspace.fry-bot.primary_shared_key
}
