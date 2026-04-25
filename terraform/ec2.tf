# 1. Obter a AMI mais recente do Amazon Linux 2023
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# 1.5 Obter a lista oficial de IPs do CloudFront gerenciada pela AWS
data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

# 2. Security Group: Permitir entrada apenas na porta HTTP para a API e SSH para emergência
resource "aws_security_group" "api_sg" {
  name        = "telco_churn_api_sg"
  description = "Permitir trafego web para a API do Telco Churn"

  ingress {
    description     = "HTTP Port for FastAPI (Only from CloudFront)"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.cloudfront.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. IAM Role: Conceder permissão para o Github Actions controlar a máquina remotamente via AWS SSM
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_ssm_role" {
  name               = "telco_churn_ec2_ssm_role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_ssm_profile" {
  name = "telco_churn_ec2_ssm_profile"
  role = aws_iam_role.ec2_ssm_role.name
}

# 4. Instância EC2 (t3.micro - Free Tier) que rodará o Docker de forma transparente
resource "aws_instance" "app_server" {
  ami                  = data.aws_ami.amazon_linux_2023.id
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.ec2_ssm_profile.name

  vpc_security_group_ids = [aws_security_group.api_sg.id]

  # User Data: Script que roda magicamente no boot da máquina
  user_data = <<-EOF
              #!/bin/bash
              
              # 1. Cria 2GB de Swap para proteger a máquina t3.micro (1GB RAM) contra OOM Killer
              dd if=/dev/zero of=/swapfile bs=128M count=16
              chmod 600 /swapfile
              mkswap /swapfile
              swapon /swapfile
              echo "/swapfile swap swap defaults 0 0" >> /etc/fstab

              # 2. Atualiza os pacotes e instala o Docker
              dnf update -y
              dnf install -y docker
              
              # Inicia o serviço do Docker
              systemctl start docker
              systemctl enable docker
              
              # Adiciona o usuário ec2-user ao grupo docker
              usermod -aG docker ec2-user
              
              # Baixa a imagem do Docker Hub e roda o container na porta 8000
              docker run -d -p 8000:8000 --restart always ${var.docker_image}
              EOF

  tags = {
    Name = "Telco-Churn-API-Serverless-Node"
  }
}

# 4. AWS ACM Certificate: Solicitando certificado SSL gratuito na Virgínia
resource "aws_acm_certificate" "api_cert" {
  provider          = aws.us_east_1
  domain_name       = "api.telcochurn.cloud-ip.cc"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# 5. AWS CloudFront: Para termos uma URL HTTPS segura e customizada
resource "aws_cloudfront_distribution" "api_cdn" {
  enabled = true
  aliases = ["api.telcochurn.cloud-ip.cc"]

  origin {
    domain_name = aws_instance.app_server.public_dns
    origin_id   = "EC2Origin"

    custom_origin_config {
      http_port              = 8000
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "EC2Origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    
    forwarded_values {
      query_string = true
      headers      = ["*"]
      cookies {
        forward = "all"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["BR", "PT"]
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.api_cert.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  
  web_acl_id = aws_wafv2_web_acl.api_waf.arn
}

# 6. AWS WAF (Web Application Firewall) para Segurança Avançada na Borda
resource "aws_wafv2_web_acl" "api_waf" {
  provider    = aws.us_east_1
  name        = "telco-churn-api-waf"
  description = "WAF para bloquear abusos e ataques contra a API"
  scope       = "CLOUDFRONT"

  default_action {
    allow {}
  }

  # Regra 1: Rate Limiting (Bloqueia IPs que fizerem mais de 100 requisições em 5 minutos)
  rule {
    name     = "RateLimitRule"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 100
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "RateLimitRuleMetric"
      sampled_requests_enabled   = false
    }
  }



  visibility_config {
    cloudwatch_metrics_enabled = false
    metric_name                = "TelcoChurnApiWafMetric"
    sampled_requests_enabled   = false
  }
}
