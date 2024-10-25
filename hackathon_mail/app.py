from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'raihanulhaque007@gmail.com'
app.config['MAIL_PASSWORD'] = 'tprq icci uieo idkw'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize Flask-Mail
mail = Mail(app)

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
        
        # Create message
        msg = Message(
            subject=data['subject'],
            sender=app.config['MAIL_USERNAME'],
            recipients=[data['recipient']]
        )
        msg.body = data['body']
        
        # Add HTML content if provided
        if 'html_content' in data:
            msg.html = data['html_content']
            
        # Add attachments if provided
        if 'attachments' in data and isinstance(data['attachments'], list):
            for attachment in data['attachments']:
                with app.open_resource(attachment['path']) as fp:
                    msg.attach(
                        filename=attachment['filename'],
                        content_type=attachment['content_type'],
                        data=fp.read()
                    )
        
        # Send email
        mail.send(msg)
        
        return jsonify({
            'message': 'Email sent successfully',
            'recipient': data['recipient']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send email',
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
    # Check if environment variables are set
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        raise ValueError(
            "Email credentials not found. Please set EMAIL_USER and EMAIL_PASSWORD in .env file"
        )
    
    app.run(debug=True)