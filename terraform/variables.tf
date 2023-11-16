variable "solution_name" {
  type        = string
  description = "The name of the solution"
  default     = "report-hub"
}

variable "org_name" {
  type        = string
  description = "The name of the organization"
  default     = "kvncont"
}

variable "environment" {
  type        = string
  description = "Environment where the solution is deployed"
  default     = "dev"
}

variable "registry_server" {
  type        = string
  description = "Server for the container registry"
  default     = "ghcr.io"
}

variable "registry_username" {
  type        = string
  description = "Username for the container registry"
  default     = "kvncont"
}

variable "registry_password" {
  type        = string
  description = "Password for the container registry"
}
