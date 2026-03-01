output "sqs_queue_url" {
  description = "Queue URL for data_producer.py"
  value       = aws_sqs_queue.main.url
}

output "s3_bucket_name" {
  value = aws_s3_bucket.events.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.processor.function_name
}

output "glue_database_name" {
  value = aws_glue_catalog_database.main.name
}

output "glue_crawler_name" {
  value = aws_glue_crawler.main.name
}