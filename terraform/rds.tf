# --- DB SUBNET GROUP ---
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [aws_subnet.private.id, aws_subnet.private_2.id] 
  # Note: RDS requires at least 2 AZs usually, but for single-AZ free tier with one subnet we might need to fake it or use 2 private/public. 
  # For assignment purposes, we list the available subnets.
  
  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# --- RDS INSTANCE ---
resource "aws_db_instance" "default" {
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "16.3"
  instance_class         = "db.t3.micro" # Free Tier eligible
  db_name                = "librarydb"
  username               = "dbadmin"
  password               = var.db_password
  parameter_group_name   = "default.postgres16"
  skip_final_snapshot    = true
  publicly_accessible    = false # Security: Private Subnet Only
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  # Security Controls (Assignment Part D)
  storage_encrypted      = true 
  multi_az               = false # Set to true for High Availability (Costs $)
}
