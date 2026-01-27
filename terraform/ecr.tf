# --- ECR REPOSITORY ---
resource "aws_ecr_repository" "app_repo" {
  name                 = "${var.project_name}-repo"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # Allow deleting even if images exist (for class cleanup)

  image_scanning_configuration {
    scan_on_push = false
  }
}

# Output the repo URL so we can use it easily
output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}
