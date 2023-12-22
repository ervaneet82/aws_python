provider "aws" {
  region = "us-east-1"  # Replace with your desired AWS region
}

variable "ingress_rules" {
  type    = list(object({
    type        = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
    {
      type        = "ingress"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      type        = "ingress"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    # Add more rules as needed...
  ]
}

resource "aws_security_group" "example" {
  name        = "example-security-group"
  description = "Example security group with dynamic rules"

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      type        = ingress.value.type
    }
  }
}

resource "aws_db_snapshot" "example_snapshot" {
  db_instance_identifier = aws_db_instance.example.identifier
  identifier            = "my-db-snapshot"
  tags                  = aws_db_instance.example.tags

  copy_tags_to_snapshot = true
}
