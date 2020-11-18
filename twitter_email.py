import smtplib
import ssl
from email.message import EmailMessage
from getpass import getpass


me = "dev.charlie.gallagher@gmail.com"
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""

msg = EmailMessage()
msg.set_content(text)

msg['Subject'] = "Hello to you"
msg['From'] = me
msg['To'] = me

g_host = 'smtp.gmail.com'
g_port = 465
g_context = ssl.create_default_context()
print(f"\nEmail: {me}")
passwd = getpass('Password: ')

# Working with API


with smtplib.SMTP_SSL(host=g_host, port=g_port, context=g_context) as g:
    g.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    g.send_message(msg)

