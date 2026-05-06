variable "aws_region" {
  description = "AWS region for the lab."
  type        = string
  default     = "eu-central-1"
}

variable "allowed_bucket_arn" {
  description = "Only this bucket can be listed and read by the IAM user."
  type        = string
  default     = "arn:aws:s3:::example-private-bucket"
}
