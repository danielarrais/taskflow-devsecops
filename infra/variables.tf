variable "region" {
  description = "Região AWS onde os recursos serão provisionados."
  type        = string
}

variable "environment" {
  description = "Nome do ambiente (ex: production, staging)."
  type        = string
}

variable "allowed_ip_cidr" {
  description = "CIDR permitido para acesso HTTPS à aplicação. Não use 0.0.0.0/0."
  type        = string

  validation {
    condition     = var.allowed_ip_cidr != "0.0.0.0/0"
    error_message = "allowed_ip_cidr não pode ser 0.0.0.0/0. Restrinja ao CIDR da sua rede."
  }
}
