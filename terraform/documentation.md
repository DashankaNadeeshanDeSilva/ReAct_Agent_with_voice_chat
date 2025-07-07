## 🏗️ What is Terraform?
Terraform is an Infrastructure as Code (IaC) tool that lets you define and manage cloud infrastructure using configuration files instead of clicking around in the AWS console.

Comparison:
* Traditional way: Manually create servers, networks, databases through web interface.
* Terraform way: Write code that describes what you want, then Terraform builds it automatically.

🎯 Key Benefits:
✅ Reproducible: Same infrastructure every time
✅ Version controlled: Track changes like code
✅ Automated: No manual clicking
✅ Consistent: Same setup across dev/staging/production

AWS Resources (created by your Terraform):
* ECR: Container storage
* ECS: Container hosting
* Load Balancer: Traffic distribution
* VPC: Network security

## Project Terraform File Structure
```bash
terraform/
├── main.tf        # Main infrastructure definitions
├── variables.tf   # Input parameters (like function parameters)
├── iam.tf        # Security permissions and roles
├── outputs.tf    # Return values after creation
└── ecs-services.tf # Container service definitions
```
🔍 Let's Break Down Each File
1. ```variables.tf``` - Configuration Parameters

```bash
variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "The environment to deploy to (dev, staging, production)"
  type        = string
  default     = "dev"
}
```

What this does:

Like function parameters for your infrastructure
Lets you customize deployments without changing the main code
You can deploy to different regions or environments just by changing these values
For KIFrag: You can easily switch between:

* ```environment = "dev"``` → Development environment
* ```environment = "production"``` → Production environment

2. ```main.tf``` - Core Infrastructure
Let me explain each section:

🌐 VPC (Virtual Private Cloud)
Real-world analogy: Like building a private office building with:

Private offices (private subnets): Where your microservices live securely
Reception area (public subnets): Where visitors (users) can access
Multiple floors (availability zones): For redundancy
For KIFrag: Creates a secure network where your 4 microservices can communicate privately.

```bash
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "kifrag-vpc-${var.environment}"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}
````
