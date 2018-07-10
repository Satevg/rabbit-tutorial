import pika
import sys

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')  # sudo rabbitmqctl list_exchanges - list exchanges

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
print(f'SEVERITY: {severity}')

channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print(f" [x] Sent {message}")

connection.close()