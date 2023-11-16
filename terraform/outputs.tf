output "container_app_fqdn" {
  value = azurerm_container_app.report_hub.latest_revision_fqdn
}
