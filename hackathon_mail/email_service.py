# email_service.py
from flask import Flask, request, jsonify
import pika
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# RabbitMQ connection configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE = 'email_queue'

def setup_rabbitmq():
    """Setup RabbitMQ connection and channel"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    
    # Declare a queue for emails
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    
    return connection, channel

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['recipient', 'subject', 'body']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields. Please provide recipient, subject, and body.'
            }), 400
            
        # Create RabbitMQ connection
        connection, channel = setup_rabbitmq()
        
        # Publish message to queue
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        # Close connection
        connection.close()
        
        return jsonify({
            'message': 'Email queued successfully',
            'recipient': data['recipient']
        }), 202
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to queue email',
            'details': str(e)
        }), 500

# Basic route for testing
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Email Service is running',
        'endpoints': {
            'send_email': '/send-email (POST)',
            'status': '/ (GET)'
        }
    })

if __name__ == '__main__':
    app.run(debug=True)