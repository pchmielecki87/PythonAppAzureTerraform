data "azurerm_key_vault" "kv" {
  name                = "sages-ado-kv"
  resource_group_name = "sages-ado-kv"
}
