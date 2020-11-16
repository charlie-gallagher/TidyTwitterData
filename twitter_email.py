import smtplib
import ssl
from email.message import EmailMessage


# me = "dev.charlie.gallagher@gmail.com"
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
#
# msg = EmailMessage()
# msg.set_content(text)
#
# msg['Subject'] = "Hello to you"
# msg['From'] = me
# msg['To'] = me
#
# g_host = 'smtp.google.com'
# g_port = 465
# g_context = ssl.create_default_context()
# print(f"\nEmail: {me}")
# passwd = input('Password: ')
#
# with smtplib.SMTP_SSL(host=g_host, port=g_port, context=g_context) as g:
#     g.login("dev.charlie.gallagher@gmail.com", passwd)
#     g.send_message(msg)

g_host = 'smtp.google.com'
g_port = 465
g_context = ssl.create_default_context()

me = "dev.charlie.gallagher@gmail.com"
other_me = "charlesjgallagher15@gmail.com"

passwd = input("Password: ")
message = """
Dear Charlie,

Be well.

Other Charlie
"""


with smtplib.SMTP_SSL(host=g_host, port=g_port, context=g_context) as g:
    g.login(me, passwd)
    g.sendmail(me, other_me, message)
