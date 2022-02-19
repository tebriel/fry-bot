terraform {
  required_version = ">= 1.1.6"
}

# Configure the Azure Provider
provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.87.0"
    }
  }
  cloud {
    organization = "tebriel"
    workspaces {
      name = "fry-bot"
    }
  }
}
