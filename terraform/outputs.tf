output "ec2_public_dns" {
  description = "Acesso direto HTTP no EC2"
  value       = "http://${aws_instance.app_server.public_dns}:8000/docs"
}

output "acm_validation_cname_name" {
  description = "NOME do Registro CNAME a ser criado no ClouDNS para a AWS liberar o certificado"
  value       = tolist(aws_acm_certificate.api_cert.domain_validation_options)[0].resource_record_name
}

output "acm_validation_cname_value" {
  description = "VALOR do Registro CNAME a ser colado no ClouDNS"
  value       = tolist(aws_acm_certificate.api_cert.domain_validation_options)[0].resource_record_value
}

# output "cloudfront_secure_url" {
#   description = "Acesso Oficial da API (HTTPS, CloudFront Gratuito)"
#   value       = "https://${aws_cloudfront_distribution.api_cdn.domain_name}/docs"
# }
