from email.message import EmailMessage
import ssl
import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""Wszystko działa wartośc mess to treśc emaila"""


def email_send(subject: str, mes: str):
    with open("./Report_crypto/email_values.json") as file:
        email_crudentials = json.load(file)

    sender = email_crudentials['sender']['login']

    for receiver in email_crudentials['reciver']:

        em = EmailMessage()
        em["From"] = sender
        em["To"] = receiver
        em["Subject"] = subject
        em.set_content(mes)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender, email_crudentials['sender']['password'])
            smtp.sendmail(sender, receiver, em.as_string())


def email_send_table(subject: str,table_data: list, mes: str=""):
    """Subject is header of email,
    table_data list with html table elements,
    mes text message before table"""

    with open("./Report_crypto/email_values.json") as file:
        email_crudentials = json.load(file)

    sender = email_crudentials['sender']['login']

    for receiver in email_crudentials['reciver']:

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver


        prep_table = f"""
        <html>
        <head></head>
        <body>
        <p>{mes}</p>
        <table border="1">
          <tr>
            {"".join([f'<th>{header}</th>' for header in table_data[0]])}
          </tr>
            {"".join(row for row in table_data[1:])}
        </table>
        </body>
        </html>
        """


        msg.attach(MIMEText(prep_table,'html'))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            # smtp.starttls()
            smtp.login(sender, email_crudentials['sender']['password'])
            smtp.sendmail(sender, receiver, msg.as_string())

# email_send_table()

























