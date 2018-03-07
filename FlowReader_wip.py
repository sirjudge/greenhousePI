# -*- coding: utf-8 -*-
import serial
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import traceback

###Variables:
ser = serial.Serial('/dev/ttyACM0',9600,timeout =10)
alreadySent = 0
count = 0
maxFlow = 100
minFlow = 10
#boolean highLow


###Functions


def sendMail(flow):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Flow out of Range"
    body = "Your water flow is out of range! Most recent reading is: " + str(flow) + " L/s. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikeplants1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()


###Main

print ( "connected to: " + ser.portstr )

while True:
    try:
        if(ser.isOpen() == 0):
            ser.baudrate = 9600
            ser.open()
            
        val = ser.readline()
        floatVal = float(val)
        print (val)
        count += 1

        
        #Too Hot Check
        if (floatVal>maxFlow):
            if(alreadySent == 0 and count > 2):
                print('Your flow is out of Range! \n')
                sendMail(floatVal)
                alreadySent = 1
        if(floatVal<maxFlow and alreadySent == 1):
            alreadySent = 0

##        #Too Cold Check
##        if (floatVal<minFlow):
##            if(alreadySent == 0 and count > 2):
##                print('Your flow is out of Range! \n')
##                sendMail(floatVal)
##                alreadySent = 1
##        if(floatVal>minFlow and alreadySent == 1):
##            alreadySent = 0

    except:
        print ("Wating for Device")
        tb = traceback.format_exc()
        print (tb)
        ser.close()
        time.sleep(5)

