import requests
import json

url = "http://localhost:5000/send-email"
payload = {
    "recipient": "raihanulhaque404@gmail.com",
    "subject": "Test Email",
    "body": "This is a test email sent via RabbitMQ",
    "html_content": "<h1>Hello</h1><p>This is HTML content</p>"  # Optional
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())