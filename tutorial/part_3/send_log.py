import pika
import sys

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')  # sudo rabbitmqctl list_exchanges - list exchanges

result = channel.queue_declare(exclusive=True)  # random queue name is in result.method.queue
                                                # exclusive=True means excusive for channel, whe connection colsed, queue deleted

channel.queue_bind(exchange='logs', queue=result.method.queue)  # bind exchange to queue, rabbitmqctl list_bindings


print(sys.argv[1:])
message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f" [x] Sent {message}")

connection.close()