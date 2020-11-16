# Email Transfer and Security
## Simple Mail Transfer Protocol (SMTP)
The Simple Mail Transfer Protocol is a method for sending and receiving emails across an internet connection. Read the [standard](https://tools.ietf.org/html/rfc821.html). Here is an ASCII diagram of the protocol:

```
            +----------+                +----------+
+------+    |          |                |          |
| User |<-->|          |      SMTP      |          |
+------+    |  Sender- |Commands/Replies| Receiver-|
+------+    |   SMTP   |<-------------->|    SMTP  |    +------+
| File |<-->|          |    and Mail    |          |<-->| File |
|System|    |          |                |          |    |System|
+------+    +----------+                +----------+    +------+


            Sender-SMTP                Receiver-SMTP
```

The user or file system sends input to the sender-SMTP, which communicates with the Receiver-SMTP and may or may not be allowed to send the email. The Sender and Receiver communicate with commands like EMAIL, OK, RCPT. Once the Receiver-SMTP gives the OK to send the email, the Sender sends the mail data, terminating with a special sequence.

Google's [SMTP](https://developers.google.com/gmail/imap/imap-smtp) server is at `smtp.google.com` port `465`.

In Python, the built-in module for dealing with SMTP is `smtplib`, which has `smtplib.SMTP` and `smtplib.SMTP_SSL`, objects that encapsulate an SMTP instance.

## Secure Sockets Layer (SSL)
SSL has a successor, TLS (Transport Layer Security). Both are "protocols for establishing authenticated and encrypted links between networked computers," ([source](https://www.ssl.com/faqs/faq-what-is-ssl/)). Simplistically, these protocols encrypt your data when it is transfered over a network.

In Python, the module for dealing with SSL is `ssl`, which contains `ssl.create_default_context()` to "load the system’s trusted CA certificates, enable host name checking and certificate validation, and try to choose reasonably secure protocol and cipher settings," ([source](https://realpython.com/python-send-email/)).

Before using `smtplib.SMTP_SSL`, you should first create an SSL context with the above function, or a customized one, and use that as the `context` argument to `SMTP_SSL`. For example:

```py
g_host = 'smtp.google.com'
g_port = 465
g_context = ssl.create_default_context()

with smtplib.SMTP_SSL(host=g_host, port=g_port, context=g_context) as g:
    g.login("dev.charlie.gallagher@gmail.com", passwd)
    g.sendmail(from_address, to_address, message)  # Diagram
```


# Formatting Emails
## Multipurpose Internet Mail Extensions (MIME)
[MIME](https://tools.ietf.org/html/rfc2045.html) is a standard for extending mail transmission to include images, sounds, and other types of multimedia.

The Python tool for handling MIME is `email`. This is a package of modules for creating, reading, decoding, and encoding emails for tranfer with SMTP. Much of it goes over my head, but there is good documentation.

### `email.message`
This module contains the class `EmailMessage`. From the `email.message` documentation:

>An email message consists of _headers_ and a _payload_ (also referred to as the _content_). Headers are RFC 5322 or RFC 6532 style field names and values, where the field name and value are separated by a colon. The colon is not part of either the field name or the field value. The payload may be a simple text message, or a binary object, or a structured sequence of sub-messages each with their own set of headers and their own payload. The latter type of payload is indicated by the message having a MIME type such as `multipart/*` or `message/rfc822`.
>
>The conceptual model provided by an `EmailMessage` object is that of an ordered dictionary of headers coupled with a _payload_ that represents the RFC 5322 body of the message, which might be a list of sub-EmailMessage objects.\[...\]
>
>The `EmailMessage` dictionary-like interface is indexed by the header names, which must be ASCII values. The values of the dictionary are strings with some extra methods. Headers are stored and returned in case-preserving form, but field names are matched case-insensitively. Unlike a real `dict`, there is an ordering to the keys, and there can be duplicate keys. Additional methods are provided for working with headers that have duplicate keys.
>
>The payload is either a `string` or `bytes` object, in the case of simple message objects, or a list of `EmailMessage` objects, for MIME container documents such as `multipart/*` and `message/rfc822` message objects.

That's a whole large chunk of documentation, but it's fairly concise all things considered.

### `email.generator`
I will be generating a flat version of the email message. From the documentation:

>One of the most common tasks is to generate the flat (serialized) version of the email message represented by a message object structure. You will need to do this if you want to send your message via smtplib.SMTP.sendmail() or the nntplib module, or print the message on the console. Taking a message object structure and producing a serialized representation is the job of the generator classes.

Probably, I will be using a `BytesGenerator` object to serialize my messages for transfer with `smtplib`.


### `email.policy`
Each email needs a policy, which includes all sorts of options for deviating from the defaults and RFCs. A potentially important default is `linesep`, which is by default `\n` (Python's own line separator). But Windows uses `\r\n` as its line separator. In general, a good policy is `email.policy.SMTP` or `email.policy.SMPTUTF8`, if UTF-8 is handled. This is a good one for me because Twitter users use lots of UTF-8 character.


### Creating a basic text and html email
```py
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a>
       has many great tutorials.
    </p>
  </body>
</html>
"""
```

Here are two items I would like to send after preparing them with `email`. How will I do this? I need to make an `email.EmailMessage` instance that contains the appropriate headers and content.

Here's an  example from the docs:

```py
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is
in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = f'The contents of {textfile}'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
```

Quickly adapting this:

```py
import smtplib
from email.message import EmailMessage

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

g_host = 'smtp.google.com'
g_port = 465
g_context = ssl.create_default_context()
passwd = input(f"Username: {me}\nPassword: ")

with smtplib.SMTP_SSL(host=g_host, port=g_port, context=g_context) as g:
    g.login("dev.charlie.gallagher@gmail.com", passwd)
    g.send_message(msg)
```

This didn't work, and I'm not sure why.
