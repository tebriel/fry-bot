resource "azurerm_resource_group" "fry-bot" {
  name     = "fry-bot"
  location = "East US 2"
}

resource "azurerm_container_group" "fry-bot" {
  name                = "fry-bot"
  resource_group_name = azurerm_resource_group.fry-bot.name
  location            = azurerm_resource_group.fry-bot.location
  os_type             = "Linux"
  restart_policy      = "Always"
  dns_name_label      = "fry-bot"

  tags = {}

  container {
    name   = "fry-bot"
    image  = "ghcr.io/tebriel/fry-bot:latest"
    cpu    = "1"
    memory = "1.5"
    environment_variables = {
      "ENVIRONMENT" = "production"
      "GITHUB_SHA"  = "unknown"
    }

    secure_environment_variables = {}

    ports {
      port     = 80
      protocol = "TCP"
    }

  }

  diagnostics {
    log_analytics {
      log_type      = "ContainerInstanceLogs"
      workspace_id  = azurerm_log_analytics_workspace.fry-bot.workspace_id
      workspace_key = azurerm_log_analytics_workspace.fry-bot.primary_shared_key
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.fry-bot.id]
  }

  timeouts {}

  lifecycle {
    ignore_changes = [image_registry_credential, container]
  }
}
resource "azurerm_user_assigned_identity" "fry-bot" {
  resource_group_name = azurerm_resource_group.fry-bot.name
  location            = azurerm_resource_group.fry-bot.location

  name = "fry-bot"
}
