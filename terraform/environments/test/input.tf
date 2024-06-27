import {
  to = azurerm_resource_group.test
  id = "/subscriptions/${var.subscription_id}/resourceGroups/${var.resource_group}"
}
# Azure GUIDS
variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}

# Resource Group/Location
variable "location" {}
variable "resource_group" {}
variable "application_type" {}

# Network
variable "virtual_network_name" {}
variable "address_prefix_test" {}
variable "address_space" {}

variable "admin_username" {}
