# This script will take a screenshot of the computer it's running on, look the color of a specified point
# If conditions are met (in this example, if the point is Red)
# Send either a simple email message, an email message with the screenshot attached, or a slack message

import email
import smtplib
import ssl
from PIL import ImageGrab
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Import separate config py file that contains private data (email addresses, slack info)
import config

######################################
# Simple Email Message (no attachment)
######################################


def sendAlertEmail():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    message = """\
        Subject: Equipment Alert

        Error detected on *Equipment Name* System."""
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, config.sender_password)
        server.sendmail(sender_email, receiver_email, message)
        print(sender_email, receiver_email, message)

######################################
# Email Message (with attachment)
######################################


def sendAlertEmailWithAttachment():
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    subject = "Equipment Alert"
    body = "Equipment Fault Detected"
    sender_email = config.sender_email
    receiver_email = config.receiver_email
    password = config.sender_password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "\\screenshot.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

######################################
# Slack Alert Message
######################################


def sendSlackMessage():
    # slack_token = os.environ["SLACK_BOT_TOKEN"]
    slack_token = config.slack_token
    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(
            channel=config.slack_channel_name,
            text="Equipment in Error State"
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        # print(e.response['error'])
        print('error')
        # str like 'invalid_auth', 'channel_not_found'
        assert e.response["error"]


# Screenshot image
im = ImageGrab.grab()

# Print out width and height of image
# w,h = im.size
# print(w,h)

# Set point of interest to get color
x = 978
y = 290
color = im.getpixel((x, y))
print(color)

# Optionally save image to send later in email
im.save('screenshot.png')
im.save('screenshot.pdf')
# im.show()

# If color conditions met, perform one of the alert notifications
# This code looks for a red color (r,g,b where r>200 and g,b <50)
if color[0] > 200 and color[1] < 50 and color[2] < 50:
    # sendAlertEmail()
    # sendAlertEmailWithAttachment()
    sendSlackMessage()
