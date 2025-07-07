# Create IAM role for ECS execution
resource "aws_iam_role" "ecs_execution_role" {
  name = "kifrag-ecs-execution-role-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach policies to ECS execution role
resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Create IAM role for ECS task
resource "aws_iam_role" "ecs_task_role" {
  name = "kifrag-ecs-task-role-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Create policy for ECS task to access Secrets Manager
resource "aws_iam_policy" "ecs_secrets_access" {
  name        = "kifrag-ecs-secrets-access-${var.environment}"
  description = "Allow ECS tasks to access secrets in Secrets Manager"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Resource = [
          "arn:aws:secretsmanager:${var.aws_region}:*:secret:kifrag-*"
        ]
      }
    ]
  })
}

# Attach secrets policy to task role
resource "aws_iam_role_policy_attachment" "task_secrets_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_secrets_access.arn
}

# Create AWS Secrets Manager secrets for each service
resource "aws_secretsmanager_secret" "agent_service_secrets" {
  name        = "kifrag-agent-service-${var.environment}"
  description = "Secrets for KIFrag Agent Service"
}

resource "aws_secretsmanager_secret" "indexing_service_secrets" {
  name        = "kifrag-indexing-service-${var.environment}"
  description = "Secrets for KIFrag Indexing Service"
}

# Create CloudWatch log groups
resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/ecs/kifrag/api-gateway-${var.environment}"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "agent_service_logs" {
  name              = "/ecs/kifrag/agent-service-${var.environment}"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "indexing_service_logs" {
  name              = "/ecs/kifrag/indexing-service-${var.environment}"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "frontend_logs" {
  name              = "/ecs/kifrag/frontend-${var.environment}"
  retention_in_days = 30
}
