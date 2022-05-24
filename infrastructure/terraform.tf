terraform {
  required_version = ">= 1.1.6"
}

# Configure the Azure Provider
provider "azurerm" {
  features {}
}
provider "github" {
  # Configuration options
}

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "4.25.0"
    }

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.7.0"
    }
  }
  cloud {
    organization = "tebriel"
    workspaces {
      name = "fry-bot"
    }
  }
}
