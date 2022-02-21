resource "github_actions_secret" "registry-url" {
  repository      = "fry-bot"
  secret_name     = "REGISTRY_URL"
  plaintext_value = "gchr.io"
}
