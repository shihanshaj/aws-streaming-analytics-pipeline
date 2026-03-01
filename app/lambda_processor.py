import json
import boto3
import base64
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    """
    Triggered automatically by Kinesis every time new data arrives.
    Processes each record and saves it to S3.
    """
    print(f"Processing {len(event['Records'])} records")
    
    processed_records = []
    failed_records = []

    for record in event['Records']:
        try:
            # Kinesis data is base64 encoded — decode it first
            raw_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            event_data = json.loads(raw_data)
            
            # Enrich the event with processing metadata
            processed_event = {
                **event_data,
                'processed_at': datetime.utcnow().isoformat(),
                'shard_id': record['eventID'],
                'sequence_number': record['kinesis']['sequenceNumber']
            }
            processed_records.append(processed_event)
            print(f"Processed event: {event_data.get('event_type')} from user {event_data.get('user_id')}")

        except Exception as e:
            print(f"Failed to process record: {e}")
            failed_records.append(record['kinesis']['sequenceNumber'])

    # Save all processed records to S3 in one batch
    if processed_records:
        save_to_s3(processed_records)

    print(f"Done. Processed: {len(processed_records)}, Failed: {len(failed_records)}")
    return {
        'statusCode': 200,
        'processed': len(processed_records),
        'failed': len(failed_records)
    }


def save_to_s3(records):
    """
    Saves records to S3 organized by date for easy querying.
    Path format: events/year=2026/month=03/day=01/timestamp.json
    """
    now = datetime.utcnow()
    
    # Partition by date — this makes Athena queries much faster
    s3_key = (
        f"events/"
        f"year={now.strftime('%Y')}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}/"
        f"{now.strftime('%H-%M-%S-%f')}.json"
    )

    # Save as newline-delimited JSON (standard for analytics)
    body = '\n'.join(json.dumps(record) for record in records)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=body,
        ContentType='application/json'
    )
    print(f"Saved {len(records)} records to s3://{BUCKET_NAME}/{s3_key}")