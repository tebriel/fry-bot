resource "github_actions_secret" "tf-api-token" {
  repository      = "fry-bot"
  secret_name     = "TF_API_TOKEN"
  plaintext_value = var.tf-api-token
}
