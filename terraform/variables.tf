variable "aws_region" {
  description = "AWS Region to deploy resources"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for resources"
  default     = "library-system"
}

variable "db_username" {
  description = "Database master username"
  default     = "dbadmin"
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  default     = "securepassword123!" 
  sensitive   = true
}

# --- COST CONTROL TOGGLES ---
variable "create_nat_gateway" {
  description = "Enable NAT Gateway? (COSTS MONEY: ~$0.045/hr). Required for private subnet internet access."
  type        = bool
  default     = false # Default to FREE mode
}

variable "enable_multi_az" {
  description = "Enable Multi-AZ for RDS? (COSTS MONEY: 2x Instance Price). Required for High Availability."
  type        = bool
  default     = false # Default to FREE mode
}
