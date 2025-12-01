variable "prefix" {
  type    = string
  default = "shopdemo"
}

variable "rg_name" {
  type    = string
  default = "shopdemo-rg"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "tags" {
  type    = map(string)
  default = {
    project = "shopping-list-demo"
    owner   = "devops"
  }
}
