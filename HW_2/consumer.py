import json
import os
import sys
import time
from mongoengine import connect
import pika

# Підключення до MongoDB
connect(db='email_contacts', host='mongodb://localhost:27017/email_contacts')

from models import Contact  # Імпорт моделі

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='web_16_queue', durable=True)


def send_email_message(contact_id):
    # Заглушка для імітації відправлення повідомлення
    print(f"Simulating sending email message to contact with ID {contact_id}")
    time.sleep(1)  # Імітація тривалості надсилання

    # Позначаємо, що повідомлення надіслано
    contact = Contact.objects.get(id=contact_id)
    contact.is_message_sent = True
    contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message['contact_id']

    try:
        send_email_message(contact_id)
        print(f" [x] Completed {method.delivery_tag} task")
    except Exception as e:
        print(f" [!] Error processing task: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='web_16_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
