output "ec2_public_dns" {
  description = "Acesso direto (HTTP, Inseguro)"
  value       = "http://${aws_instance.app_server.public_dns}:8000/docs"
}

output "cloudfront_secure_url" {
  description = "Acesso Oficial da API (HTTPS, CloudFront Gratuito)"
  value       = "https://${aws_cloudfront_distribution.api_cdn.domain_name}/docs"
}
