## RG ##################################################################
resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
  tags     = var.tags
}

## WEBAPP ##################################################################
resource "azurerm_service_plan" "asp" {
  name                = "${var.prefix}-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "F1" # Free tier App Service Plan
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "${var.prefix}-law"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku               = "PerGB2018" #Free <-- not free anymore
  retention_in_days = var.retention_in_days
}

resource "azurerm_linux_web_app" "app" {
  name                = "${var.prefix}-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    always_on = false
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.ai.connection_string
    "WEBSITE_RUN_FROM_PACKAGE"              = "1"
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.ai.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=${azurerm_application_insights.ai.instrumentation_key}"
    "PYTHON_VERSION"                        = "3.11"
    "KEYVAULT_URI"                          = data.azurerm_key_vault.kv.vault_uri
    "SCM_DO_BUILD_DURING_DEPLOYMENT"  = true
  }

  tags = var.tags

  depends_on = [azurerm_service_plan.asp, azurerm_application_insights.ai]
}

## AI ##################################################################
resource "azurerm_application_insights" "ai" {
  name                = "${var.prefix}-ai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  application_type = "web"
  workspace_id     = azurerm_log_analytics_workspace.law.id

  daily_data_cap_in_gb                  = 0.1
  daily_data_cap_notifications_disabled = true

  depends_on = [azurerm_log_analytics_workspace.law]
}