import pika
import json
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'raihanulhaque007@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'tprq icci uieo idkw'  # Replace with your password (or app password)
app.config['MAIL_DEFAULT_SENDER'] = 'raihanulhaque007@gmail.com'  # Replace with your email

mail = Mail(app)

# RabbitMQ Configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'email_queue'

def callback(ch, method, properties, body):
    print("Received message from queue")
    email_data = json.loads(body)
    
    with app.app_context():
        try:
            # Create the email message
            msg = Message(email_data['subject'], recipients=[email_data['recipient']])
            msg.body = email_data['body']

            # Send the email
            mail.send(msg)
            print(f"Email sent to {email_data['recipient']}")
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    # Acknowledge the message was processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Consume messages from the queue
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
