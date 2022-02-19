resource "github_actions_secret" "storage-connection-string" {
  repository      = "fry-bot"
  secret_name     = "STORAGE_CONNECTION_STRING"
  plaintext_value = azurerm_storage_account.fry-bot.primary_connection_string
}

resource "github_actions_secret" "registry-url" {
  repository      = "fry-bot"
  secret_name     = "REGISTRY_URL"
  plaintext_value = "gchr.io"
}
