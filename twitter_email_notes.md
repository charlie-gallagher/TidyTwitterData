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

The Python tool for handling MIME is `email`. 
