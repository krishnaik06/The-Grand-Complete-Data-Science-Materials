variable "agent_count" {
  default = 1
}

# The following two variable declarations are placeholder references.
# Set the values for these variable in terraform.tfvars
variable "aks_service_principal_app_id" {
  default = "d5fd9002-e379-4f48-8a34-c2e10119f81b"
}

variable "aks_service_principal_client_secret" {
  default = "tbV8Q~ka_FZ-I8Kw1HQbpOf15ExJrehPDme8VaJG"
}

variable "admin_username" {
  default = "demo"
}

variable "cluster_name" {
  default = "demok8s"
}

variable "dns_prefix" {
  default = "demok8s"
}

# # Refer to https://azure.microsoft.com/global-infrastructure/services/?products=monitor for available Log Analytics regions.
# variable "log_analytics_workspace_location" {
#   default = "West Europe"
# }

# variable "log_analytics_workspace_name" {
#   default = "testLogAnalyticsWorkspaceName"
# }

# # Refer to https://azure.microsoft.com/pricing/details/monitor/ for Log Analytics pricing
# variable "log_analytics_workspace_sku" {
#   default = "PerGB2018"
# }

variable "resource_group_location" {
  default     = "West Europe"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  default     = "rohan_new"
  description = "Resource group name that is unique in your Azure subscription."
}

variable "ssh_public_key" {
  default = "/Users/rohanpatankar/azure_tf.pub"
}