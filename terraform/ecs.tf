# --- ECS CLUSTER ---
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# --- LOAD BALANCER (ALB) ---
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [aws_subnet.public.id, aws_subnet.private.id] # ALB needs 2 subnets usually
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project_name}-tg"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# --- ECS TASK DEFINITION ---
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name  = "library-app"
      image = "library-app:latest" # Replace with ECR URL in real deployment
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
      environment = [
        {
          name  = "SQLALCHEMY_DATABASE_URI"
          value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.default.endpoint}/librarydb"
        }
      ]
    }
  ])
}

# --- ECS SERVICE ---
resource "aws_ecs_service" "main" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.private.id]
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false # True if in public subnet, False if private (requires NAT)
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "library-app"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener.front_end]
}
