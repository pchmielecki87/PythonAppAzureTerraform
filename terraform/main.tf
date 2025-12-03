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

# resource "azurerm_log_analytics_workspace" "law" {
#   name                = "workspace-test"
#   location            = azurerm_resource_group.example.location
#   resource_group_name = azurerm_resource_group.example.name
#   sku                 = "PerGB2018"
#   retention_in_days   = 30
# }

# resource "azurerm_application_insights" "ai" {
#   name                = "${var.prefix}-ai"
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   application_type    = "web"
#   workspace_id        = azurerm_log_analytics_workspace.law.id
#   # retention_in_days optional

#   depends_on = [azurerm_log_analytics_workspace.law]
# }

resource "azurerm_linux_web_app" "app" {
  name                = "${var.prefix}-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id = azurerm_service_plan.asp.id

  site_config {
    always_on = false
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE"           = "1"
    "APPINSIGHTS_INSTRUMENTATIONKEY"     = azurerm_application_insights.ai.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=${azurerm_application_insights.ai.instrumentation_key}"
    "PYTHON_VERSION"                     = "3.11"
  }
  
  tags = var.tags

  depends_on = [azurerm_service_plan.asp]
}
