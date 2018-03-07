
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def sendTestMail():


    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"

    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Test Email"
    body = "Your pi is connected to the network and sending emails"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

sendTestMail()
