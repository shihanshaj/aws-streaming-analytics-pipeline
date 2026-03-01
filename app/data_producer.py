import json
import boto3
import random
import time
import uuid
from datetime import datetime, timezone

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = None

def get_queue_url():
    global QUEUE_URL
    response = sqs.get_queue_url(QueueName='analytics-queue')
    QUEUE_URL = response['QueueUrl']
    print(f"Connected to queue: {QUEUE_URL}")

USER_IDS   = [f"user_{i:04d}" for i in range(1, 51)]
PAGES      = ["/home", "/products", "/cart", "/checkout", "/about", "/blog"]
PRODUCTS   = ["laptop", "phone", "headphones", "keyboard", "monitor", "mouse"]
EVENT_TYPES = ["page_view", "click", "add_to_cart", "purchase", "search"]
COUNTRIES  = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "BR"]

def generate_event():
    event_type = random.choice(EVENT_TYPES)
    event = {
        "event_id":   str(uuid.uuid4()),
        "event_type": event_type,
        "user_id":    random.choice(USER_IDS),
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "page":       random.choice(PAGES),
        "country":    random.choice(COUNTRIES),
        "session_id": str(uuid.uuid4())[:8],
    }
    if event_type == "purchase":
        event["product"]  = random.choice(PRODUCTS)
        event["amount"]   = round(random.uniform(9.99, 999.99), 2)
        event["currency"] = "USD"
    elif event_type == "add_to_cart":
        event["product"]  = random.choice(PRODUCTS)
        event["quantity"] = random.randint(1, 5)
    elif event_type == "search":
        event["query"] = random.choice(PRODUCTS)
    return event

def send_to_sqs(event):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(event)
    )

def main():
    get_queue_url()
    print("🚀 Starting data producer — sending events to SQS")
    print("Press Ctrl+C to stop\n")

    count = 0
    while True:
        try:
            batch_size = random.randint(1, 5)
            for _ in range(batch_size):
                event = generate_event()
                send_to_sqs(event)
                count += 1
                print(f"[{count}] Sent: {event['event_type']:15} | user: {event['user_id']} | page: {event.get('page', 'N/A')}")

            time.sleep(random.uniform(1, 3))

        except KeyboardInterrupt:
            print(f"\n✅ Stopped. Total events sent: {count}")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()