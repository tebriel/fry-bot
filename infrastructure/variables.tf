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

variable "tebriel-id" {
  description = "Tebriel's Object ID"
  type = string
  default = "5fd8e33b-c116-44b7-b73d-b0c9b568d58b"
}
