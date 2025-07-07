output "alb_dns_name" {
  description = "The DNS name of the application load balancer"
  value       = aws_lb.kifrag_alb.dns_name
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.kifrag_cluster.name
}

output "ecr_repository_urls" {
  description = "The URLs of the ECR repositories"
  value = {
    api_gateway      = aws_ecr_repository.api_gateway.repository_url
    agent_service    = aws_ecr_repository.agent_service.repository_url
    indexing_service = aws_ecr_repository.indexing_service.repository_url
    frontend         = aws_ecr_repository.frontend.repository_url
  }
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = module.vpc.public_subnets
}
