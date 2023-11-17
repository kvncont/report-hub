terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.80.0"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  name = "${var.org_name}-${var.solution_name}-${var.environment}"
}

resource "azurerm_resource_group" "report_hub" {
  name     = "rg-${local.name}"
  location = "eastus2"
}

resource "azurerm_log_analytics_workspace" "report_hub" {
  name                = "log-${local.name}"
  location            = azurerm_resource_group.report_hub.location
  resource_group_name = azurerm_resource_group.report_hub.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "report_hub" {
  name                       = "cae-${local.name}"
  location                   = azurerm_resource_group.report_hub.location
  resource_group_name        = azurerm_resource_group.report_hub.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.report_hub.id
}

resource "azurerm_container_app" "report_hub" {
  name                         = "ca-${local.name}"
  container_app_environment_id = azurerm_container_app_environment.report_hub.id
  resource_group_name          = azurerm_resource_group.report_hub.name
  revision_mode                = "Single"

  ingress {
    target_port      = 80
    external_enabled = true
    traffic_weight {
      percentage = 100
    }
  }

  template {
    container {
      name   = var.solution_name
      image  = "kvncont/report-hub/report-hub:16.6900694147"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  secret {
    name  = "registry-password"
    value = var.registry_password
  }

  registry {
    server               = var.registry_server
    username             = var.registry_username
    password_secret_name = "registry-password"
  }
}
