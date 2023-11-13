import json
from datetime import datetime
from mongoengine import connect, Document, StringField, BooleanField
import pika

# Підключення до MongoDB
connect(db='email_contacts', host='mongodb://localhost:27017/email_contacts')


# Модель для контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    is_message_sent = BooleanField(default=False)


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Web16 exchange', exchange_type='direct')
channel.queue_declare(queue='web_16_queue', durable=True)
channel.queue_bind(exchange='Web16 exchange', queue='web_16_queue')


def create_fake_contacts(nums: int):
    for i in range(nums):
        contact = Contact(
            full_name=f"User{i}",
            email=f"user{i}@example.com"
        ).save()

        message = {
            'contact_id': str(contact.id),
            'payload': f"Date: {datetime.now().isoformat()}"
        }

        channel.basic_publish(exchange='Web16 exchange', routing_key='web_16_queue', body=json.dumps(message).encode())

    connection.close()


if __name__ == '__main__':
    create_fake_contacts(5)
