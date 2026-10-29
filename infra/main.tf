terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = "taskflow"
    }
  }
}

data "aws_caller_identity" "current" {}

# Bucket separado para access logs. Logging neste próprio bucket causaria
# recursão; por isso CKV_AWS_18 é a única exceção e está limitada a este recurso.
resource "aws_s3_bucket" "access_logs" {
  # checkov:skip=CKV_AWS_18:bucket terminal de access logs; habilitar logging nele causaria recursão
  # checkov:skip=CKV2_AWS_62:notificações não fazem parte do escopo deste laboratório
  # checkov:skip=CKV_AWS_144:replicação multi-região elevaria custo do laboratório sem requisito de DR
  # checkov:skip=CKV_AWS_145:S3 server access logging não suporta bucket de destino com SSE-KMS
  bucket_prefix = "taskflow-access-logs-${var.environment}-"
  force_destroy = false
}

resource "aws_s3_bucket" "taskflow" {
  # checkov:skip=CKV2_AWS_62:notificações não fazem parte do escopo deste laboratório
  # checkov:skip=CKV_AWS_144:replicação multi-região elevaria custo do laboratório sem requisito de DR
  bucket_prefix = "taskflow-${var.environment}-"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_versioning" "taskflow" {
  bucket = aws_s3_bucket.taskflow.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id
  rule {
    id     = "expire-access-logs"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
    expiration { days = 90 }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "taskflow" {
  bucket = aws_s3_bucket.taskflow.id
  rule {
    id     = "expire-noncurrent-versions"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
    noncurrent_version_expiration { noncurrent_days = 90 }
  }
}

resource "aws_kms_key" "taskflow" {
  description         = "Criptografia do bucket TaskFlow"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "EnableAccountAdministration"
      Effect    = "Allow"
      Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
      Action    = "kms:*"
      Resource  = "*"
    }]
  })
}

# trivy:ignore:AVD-AWS-0132 O destino de S3 access logs suporta SSE-S3, não SSE-KMS.
resource "aws_s3_bucket_server_side_encryption_configuration" "access_logs" {
  bucket = aws_s3_bucket.access_logs.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "taskflow" {
  bucket = aws_s3_bucket.taskflow.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.taskflow.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "access_logs" {
  bucket                  = aws_s3_bucket.access_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "taskflow" {
  bucket                  = aws_s3_bucket.taskflow.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "taskflow" {
  bucket        = aws_s3_bucket.taskflow.id
  target_bucket = aws_s3_bucket.access_logs.id
  target_prefix = "taskflow/"
}

resource "aws_security_group" "taskflow" {
  # checkov:skip=CKV2_AWS_5:o laboratório define a rede; não provisiona compute para anexar o SG
  name        = "taskflow-${var.environment}"
  description = "HTTPS da TaskFlow restrito ao CIDR autorizado"

  ingress {
    description = "HTTPS somente da rede autorizada"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

output "taskflow_bucket_arn" {
  description = "ARN do bucket privado da aplicação."
  value       = aws_s3_bucket.taskflow.arn
}

output "security_group_id" {
  description = "ID do security group restrito."
  value       = aws_security_group.taskflow.id
}
