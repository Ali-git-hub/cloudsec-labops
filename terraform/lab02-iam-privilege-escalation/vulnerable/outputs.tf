output "developer_user_name" {
  value = aws_iam_user.developer.name
}

output "access_key_id" {
  value     = aws_iam_access_key.developer_key.id
  sensitive = true
}

output "secret_access_key" {
  value     = aws_iam_access_key.developer_key.secret
  sensitive = true
}
