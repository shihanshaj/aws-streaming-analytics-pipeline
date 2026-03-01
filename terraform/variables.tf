variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name prefix for all resources"
  default     = "analytics"
}

variable "queue_name" {
  description = "SQS queue name"
  default     = "analytics-queue"
}

variable "s3_bucket_name" {
  description = "S3 bucket for storing events — must be globally unique"
  default     = "analytics-events-shihan-2026"
}