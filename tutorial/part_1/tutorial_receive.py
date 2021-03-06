import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()