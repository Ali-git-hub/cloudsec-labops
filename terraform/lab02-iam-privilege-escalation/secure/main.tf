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
  name = "cloudsec-labops-readonly-dev-user"
}

resource "aws_iam_policy" "least_privilege_s3_readonly_policy" {
  name        = "cloudsec-labops-s3-readonly-policy"
  description = "Least-privilege policy for Lab 02."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListOnlySpecificBucket"
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = var.allowed_bucket_arn
      },
      {
        Sid    = "ReadOnlyObjectsInSpecificBucket"
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = "${var.allowed_bucket_arn}/*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "developer_s3_readonly_access" {
  user       = aws_iam_user.developer.name
  policy_arn = aws_iam_policy.least_privilege_s3_readonly_policy.arn
}
