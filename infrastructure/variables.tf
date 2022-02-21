variable "BOT_GATEWAY_TOKEN" {
  description = "Token for the Bot Gateway"
  type        = string
  sensitive   = true
}

variable "tf-api-token" {
  description = "API Token for Terraform"
  type        = string
  sensitive   = true
}
