import sys
import os
import json
from email.message import EmailMessage
from aiosmtplib import send
import asyncio
from datetime import datetime


SMTP_HOST=""
SMTP_PORT=465
SMTP_USERNAME=""
SMTP_PASSWORD=""
MAIL_FROM=""


async def send_email(to, subject, body_data):
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content("Plain text fallback.")

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>{subject}</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f4;
          padding: 20px;
          margin: 0;
        }}
        .email-container {{
          background-color: #ffffff;
          max-width: 600px;
          margin: 0 auto;
          padding: 30px;
          border-radius: 8px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        h2 {{
          color: #006B66;
          margin-top: 0;
        }}
        ul {{
          padding-left: 20px;
        }}
        li {{
          margin-bottom: 10px;
        }}
        .footer {{
          margin-top: 30px;
          font-size: 12px;
          color: #999999;
          text-align: center;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <h2>{subject}</h2>
        <p>Received a new inquiry with the following details:</p>
        <ul>
          <li><strong>First Name:</strong> {body_data['firstName']}</li>
          <li><strong>Last Name:</strong> {body_data['lastName']}</li>
          <li><strong>Email:</strong> {body_data['email']}</li>
          <li><strong>Phone Number:</strong> {body_data['number']}</li>
          <li><strong>Message:</strong> {body_data['message']}</li>
        </ul>
        <div class="footer">
          &copy; {datetime.now().year} Your Company. All rights reserved.
        </div>
      </div>
    </body>
    </html>
    """
    message.add_alternative(html_body, subtype="html")

    try:
        await send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            use_tls=True,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
        )
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)


def main(environ, start_response):
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b'Only POST is allowed']

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)

        required_fields = ['to', 'subject', 'firstName', 'lastName', 'email', 'number', 'message']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required field(s)")

        success, result = asyncio.run(send_email(data['to'], data['subject'], data))

        status = '200 OK' if success else '500 Internal Server Error'
        start_response(status, [('Content-Type', 'application/json')])
        return [json.dumps({'message': result}).encode()]

    except Exception as e:
        start_response('400 Bad Request', [('Content-Type', 'application/json')])
        return [json.dumps({'error': str(e)}).encode()]
