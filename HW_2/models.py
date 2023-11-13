from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    message_sent = BooleanField(default=False)

    def __str__(self):
        return f"{self.fullname} ({self.email}) - Message Sent: {self.message_sent}"
