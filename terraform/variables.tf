variable "prefix" {
  type    = string
  default = null
}

variable "rg_name" {
  type    = string
  default = null
}

variable "location" {
  type    = string
  default = null
}

variable "retention_in_days" {
  type    = string
  default = {}
}

variable "tags" {
  type    = map(string)
  default = {}
}