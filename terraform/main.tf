provider "aws" {
  region = var.aws_region
}

# VPC (Virtual Private Cloud) and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "kifrag-vpc-${var.environment}"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"
  
  tags = {
    Environment = var.environment
    Project     = "KIFrag"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "kifrag_cluster" {
  name = "kifrag-${var.environment}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Environment = var.environment
    Project     = "KIFrag"
  }
}

# ECR Repositories
resource "aws_ecr_repository" "agent_service" {
  name = "kifrag-agent-service"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "api_gateway" {
  name = "kifrag-api-gateway"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "indexing_service" {
  name = "kifrag-indexing-service"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "frontend" {
  name = "kifrag-frontend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# Security group for ECS services
resource "aws_security_group" "ecs_sg" {
  name        = "kifrag-ecs-sg-${var.environment}"
  description = "Security group for KIFrag ECS services"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"] # Only internal traffic
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Application Load Balancer
resource "aws_lb" "kifrag_alb" {
  name               = "kifrag-alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = module.vpc.public_subnets
  
  tags = {
    Environment = var.environment
    Project     = "KIFrag"
  }
}

# ALB Security Group
resource "aws_security_group" "alb_sg" {
  name        = "kifrag-alb-sg-${var.environment}"
  description = "Security group for KIFrag ALB"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
