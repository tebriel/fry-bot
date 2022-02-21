resource "azurerm_search_service" "haiku" {
  name                = "haiku-search-service"
  resource_group_name = azurerm_resource_group.fry-bot.name
  location            = "westus2" # this is the only location where the API is available
  sku                 = "free"
  replica_count       = 1
  partition_count     = 1
}

resource "azurerm_role_assignment" "haiku-search" {
  for_each = toset([
    azurerm_user_assigned_identity.fry-bot.principal_id,
    var.tebriel-id,
  ])

  scope                = azurerm_search_service.haiku.id
  role_definition_name = "Search Index Data Reader"
  principal_id         = each.key
}
