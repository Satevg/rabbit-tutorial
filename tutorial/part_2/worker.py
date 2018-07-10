import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # send signal that task completed: Important if worker dies
    # sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged - hung tasks, unack messages

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit1', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


###
# tells RabbitMQ not to give more than one message to a worker at a time.
# don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
# Instead, it will dispatch it to the next worker that is not still busy.
# (instead of default round robin strategy for workers)
###
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback, queue='task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()