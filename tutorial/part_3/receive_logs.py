import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout') #  recieiver declares queue, send to fanout exchange sends message to each receiver
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)
print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()