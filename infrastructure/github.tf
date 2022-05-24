resource "github_actions_secret" "tf-api-token" {
  repository      = "fry-bot"
  secret_name     = "TF_API_TOKEN"
  plaintext_value = var.tf-api-token
}

resource "github_actions_secret" "workspace-key" {
  repository      = "fry-bot"
  secret_name     = "WORKSPACE_KEY"
  plaintext_value = azurerm_log_analytics_workspace.fry-bot.primary_shared_key
}
