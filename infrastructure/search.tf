resource "azurerm_search_service" "haiku" {
  name                = "haiku-search-service"
  resource_group_name = azurerm_resource_group.fry-bot.name
  location            = "westus2" # this is the only location where the API is available
  sku                 = "free"
}
