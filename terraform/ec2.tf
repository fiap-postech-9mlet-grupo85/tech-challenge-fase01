# 1. Obter a AMI mais recente do Amazon Linux 2023
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# 2. Security Group: Permitir entrada apenas na porta HTTP para a API e SSH para emergência
resource "aws_security_group" "api_sg" {
  name        = "telco_churn_api_sg"
  description = "Permitir trafego web para a API do Telco Churn"

  ingress {
    description = "HTTP Port for FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # O ideal seria apenas o range do CloudFront, mas simplificamos para o Free Tier
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Instância EC2 (T2.Micro - Free Tier) que rodará o Docker de forma transparente
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux_2023.id
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.api_sg.id]

  # User Data: Script que roda magicamente no boot da máquina
  user_data = <<-EOF
              #!/bin/bash
              # Atualiza os pacotes e instala o Docker
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

# 4. AWS CloudFront: Para termos uma URL HTTPS segura, mascarando o IP sujo do EC2
resource "aws_cloudfront_distribution" "api_cdn" {
  enabled = true

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
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
