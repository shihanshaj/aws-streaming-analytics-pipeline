# aws-streaming-analytics-pipeline
A script pretends to be a website generating live user events (clicks, purchases). Kinesis captures them in real time. Lambda processes each event. S3 stores everything. Glue catalogs it. Athena lets you query it with SQL like a database.
