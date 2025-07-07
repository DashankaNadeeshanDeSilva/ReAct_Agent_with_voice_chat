variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "The environment to deploy to (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "app_image_tag" {
  description = "The Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "api_gateway_cpu" {
  description = "CPU units for the API Gateway service"
  type        = number
  default     = 256
}

variable "api_gateway_memory" {
  description = "Memory for the API Gateway service in MiB"
  type        = number
  default     = 512
}

variable "agent_service_cpu" {
  description = "CPU units for the Agent Service"
  type        = number
  default     = 1024
}

variable "agent_service_memory" {
  description = "Memory for the Agent Service in MiB"
  type        = number
  default     = 2048
}

variable "indexing_service_cpu" {
  description = "CPU units for the Indexing Service"
  type        = number
  default     = 512
}

variable "indexing_service_memory" {
  description = "Memory for the Indexing Service in MiB"
  type        = number
  default     = 1024
}

variable "frontend_cpu" {
  description = "CPU units for the Frontend service"
  type        = number
  default     = 256
}

variable "frontend_memory" {
  description = "Memory for the Frontend service in MiB"
  type        = number
  default     = 512
}
