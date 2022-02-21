resource "github_actions_secret" "registry-url" {
  repository      = "fry-bot"
  secret_name     = "REGISTRY_URL"
  plaintext_value = "gchr.io"
}

resource "github_actions_secret" "tf-api-token" {
  repository      = "fry-bot"
  secret_name     = "TF_API_TOKEN"
  plaintext_value = var.tf-api-token
}
