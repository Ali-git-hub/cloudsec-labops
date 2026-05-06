output "bucket_name" {
  value = aws_s3_bucket.public_bucket.bucket
}

output "public_object_url" {
  value = "https://${aws_s3_bucket.public_bucket.bucket}.s3.amazonaws.com/demo.txt"
}
