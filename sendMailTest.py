import smtplib



def sendMail():
    FROM = 'GoucherGreenhouseMonitor@gmail.com'
    TO = ["besae001@mail.goucher.edu"]
    Subject = "Temp Range Test Email - Phyton"
    Text = "Your temperature is out of range! Please address this immediately"

    message = """\
    From: %s
    To: %s
    Subject %s

    %s
    """ % (FROM, ", ".join(TO), Subject, Text)
    
    server = smtplib.SMTP('myserver')
    server.sendmail(FROM, TO, message)
    server.quit()

sendMail()
