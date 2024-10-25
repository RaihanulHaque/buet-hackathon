import pika
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure, random key in production

# RabbitMQ Configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'email_queue'

def send_to_queue(recipient, subject, body):
    # Establish connection with RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Create a message to send to the queue
    message = json.dumps({
        'recipient': recipient,
        'subject': subject,
        'body': body
    })

    # Publish the message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['email']
        subject = request.form['subject']
        body = request.form['message']

        try:
            # Send message to RabbitMQ queue
            send_to_queue(recipient, subject, body)
            flash('Email request sent to the queue!', 'success')
        except Exception as e:
            flash(f'Failed to send email request: {str(e)}', 'danger')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    #  LALALAALALALALALALALALALALALA
