import pika
import sys

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # Durable - store queue even if RabbitMQ crashed/restarted

print(sys.argv[1:])
message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='', routing_key='task_queue', body=message,
                      properties=pika.BasicProperties(delivery_mode=2))  # store message even if RabbitMQ restarted
print(f" [x] Sent {message}")

connection.close()