resource "github_actions_secret" "storage-url" {
  repository      = "fry-bot"
  secret_name     = "STORAGE_BASE_URL"
  plaintext_value = azurerm_storage_account.fry-bot.primary_table_host
}

resource "github_actions_secret" "registry-url" {
  repository      = "fry-bot"
  secret_name     = "REGISTRY_URL"
  plaintext_value = "gchr.io"
}
