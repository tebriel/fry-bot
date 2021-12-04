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
    image  = "${data.azurerm_container_registry.acr.login_server}/fry-bot/fry-bot:latest"
    cpu    = "1"
    memory = "1.5"
    environment_variables = {

    }

    secure_environment_variables = {
      BOT_GATEWAY_TOKEN               = var.BOT_GATEWAY_TOKEN
      AZURE_STORAGE_CONNECTION_STRING = azurerm_storage_account.cool-beans.primary_connection_string
    }

    ports {
      port     = 80
      protocol = "TCP"
    }
  }

  image_registry_credential {
    server   = data.azurerm_container_registry.acr.login_server
    username = data.azurerm_container_registry.acr.admin_username
    password = data.azurerm_container_registry.acr.admin_password
  }

  timeouts {}

  lifecycle {
    ignore_changes = [image_registry_credential, container]
  }
}