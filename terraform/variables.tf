variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "sa-east-1"
}

variable "docker_image" {
  description = "Imagem do Docker Hub a ser baixada e executada"
  type        = string
  default     = "fiappostech9mletgrupo32/telco-churn-api:latest"
}
