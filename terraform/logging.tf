# --- CLOUDWATCH LOG GROUP ---
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7
}

# --- S3 BUCKET (For Audit/Backups) ---
resource "aws_s3_bucket" "logs_bucket" {
  bucket = "${var.project_name}-logs-${random_string.suffix.result}"
  force_destroy = true # Allow easy cleanup for assignment
}

# Random suffix because S3 names must be globally unique
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# --- S3 SERVER-SIDE ENCRYPTION ---
resource "aws_s3_bucket_server_side_encryption_configuration" "logs_bucket_encryption" {
  bucket = aws_s3_bucket.logs_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# --- S3 PUBLIC ACCESS BLOCK (Security Best Practice) ---
resource "aws_s3_bucket_public_access_block" "logs_bucket_access" {
  bucket = aws_s3_bucket.logs_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
