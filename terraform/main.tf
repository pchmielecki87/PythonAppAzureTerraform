resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
  tags     = var.tags
}

resource "azurerm_service_plan" "asp" {
  name                = "${var.prefix}-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type = "Linux"
  sku_name = "F1"   # Free tier App Service Plan
}

resource "azurerm_application_insights" "ai" {
  name                = "${var.prefix}-ai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
  # retention_in_days optional
}

resource "azurerm_app_service" "app" {
  name                = "${var.prefix}-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_service_plan.asp.id

  site_config {
    linux_fx_version = "PYTHON|3.11"
    # startup command, use gunicorn
    # If you want to use default startup detection, remove startup_command
    #startup_command = "gunicorn --bind 0.0.0.0 --timeout 600 app:app"
    always_on = false
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE"           = "1"
    "APPINSIGHTS_INSTRUMENTATIONKEY"     = azurerm_application_insights.ai.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=${azurerm_application_insights.ai.instrumentation_key}"
    "PYTHON_VERSION"                     = "3.11"
  }

  tags = var.tags
}

output "app_default_site_hostname" {
  value = azurerm_app_service.app.default_site_hostname
}

output "app_insights_instrumentation_key" {
  value = azurerm_application_insights.ai.instrumentation_key
}
