# email_worker.py
import pika
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'raihanulhaque007@gmail.com'
EMAIL_PASSWORD = 'tprq icci uieo idkw'

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE = 'email_queue'

def send_email(recipient, subject, body, html_content=None):
    """Send email using Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = recipient
        
        # Add plain text body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add HTML content if provided
        if html_content:
            msg.attach(MIMEText(html_content, 'html'))
        
        # Create SMTP connection
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
            
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def callback(ch, method, properties, body):
    """Process messages from RabbitMQ queue"""
    try:
        # Parse message data
        data = json.loads(body)
        
        # Extract email details
        recipient = data['recipient']
        subject = data['subject']
        body = data['body']
        html_content = data.get('html_content')
        
        # Send email
        success = send_email(recipient, subject, body, html_content)
        
        if success:
            print(f"Email sent successfully to {recipient}")
            # Acknowledge message only if email was sent successfully
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Negative acknowledgment to requeue the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        # Negative acknowledgment to requeue the message
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    # Validate environment variables
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError(
            "Email credentials not found. Please set EMAIL_USER and EMAIL_PASSWORD in .env file"
        )
    
    while True:
        try:
            # Create connection to RabbitMQ
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            channel = connection.channel()
            
            # Declare queue
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            
            # Configure worker to process one message at a time
            channel.basic_qos(prefetch_count=1)
            
            # Set up consumer
            channel.basic_consume(
                queue=RABBITMQ_QUEUE,
                on_message_callback=callback
            )
            
            print("Email worker started. Waiting for messages...")
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError:
            print("Lost connection to RabbitMQ. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Worker stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()