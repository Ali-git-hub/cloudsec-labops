output "developer_user_name" {
  value = aws_iam_user.developer.name
}

output "policy_name" {
  value = aws_iam_policy.least_privilege_s3_readonly_policy.name
}
