data "azurerm_resource_group" "froudx-in" {
  name = "frodux.in"
}

data "azurerm_container_registry" "acr" {
  name                = "FroduxContainerRegistry"
  resource_group_name = data.azurerm_resource_group.froudx-in.name
}