import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Secrets import secrets


smtp_server = secrets["SMTP_SERVER"]
port = secrets["PORT"]
sender_email = secrets["MAIL"]
email_password = secrets["PASSWORD"]
domain = secrets["DOMAIN"];

# Create a secure SSL context
context = ssl.create_default_context()

# Create the body of the message (a plain-text and an HTML version).
link = "https://raumbuchung.bibliothek.kit.edu/sitzplatzreservierung/report.php?";
html_template = """\
<html>
  <head></head>
  <body>
    <p>Hi {name},</p>
    <p>deine aktuellen Buchungen wie folgt.</p>
    {table}
    <a href="{link}">{link}</a>
    <p>Liebe Grüße Flo :))</p>
  </body>
</html>
"""


def sendMail(receiver, name, date, html_table):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver;
    msg['Subject'] = "Neue Sitzplatzbuchung am " + date.strftime("%b-%d-%Y");
    html = html_template.format(table = html_table, name = name, link = link);
  
    # Add an SPF header to the message
    msg['SPF'] = 'v=spf1 include:' + domain+  '-all'

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(link, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()

    # Try to log in to server and send email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.close()
        print("Mail send to " + receiver);