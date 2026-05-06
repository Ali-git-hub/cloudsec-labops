terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_user" "developer" {
  name = "cloudsec-labops-dev-user"
}

resource "aws_iam_policy" "dangerous_admin_policy" {
  name        = "cloudsec-labops-dangerous-admin-policy"
  description = "Intentionally vulnerable policy for Lab 02."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "FullAdminAccess"
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "developer_admin_access" {
  user       = aws_iam_user.developer.name
  policy_arn = aws_iam_policy.dangerous_admin_policy.arn
}

resource "aws_iam_access_key" "developer_key" {
  user = aws_iam_user.developer.name
}
