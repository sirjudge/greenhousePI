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
maxTemp = 82
minTemp = 70
#boolean highLow


###Functions


def sendMail(temperature):

#can add in a highLow parameter to print the temperature is too high or too low rather than just the temp is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Temp out of Range"
    body = "Your temperature is out of range! Most recent reading is: " + str(temperature) + " deg F. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

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
        intVal = int(val)
        print (val)
        count += 1

        
        #Too Hot Check
        if (intVal>maxTemp):
            if(alreadySent == 0 and count > 2):
                print('Your temp is out of Range! \n')
                #highLow = true
                sendMail(intVal)
                alreadySent = 1
        if(intVal<maxTemp and alreadySent == 1):
            alreadySent = 0

##        #Too Cold Check
##        if (intVal<minTemp):
##            if(alreadySent == 0 and count > 2):
##                print('Your temp is out of Range! \n')
##                #highLow = false
##                sendMail(intVal)
##                alreadySent = 1
##        if(intVal>minTemp and alreadySent == 1):
##            alreadySent = 0

    except:
        print ("Wating for Device")
        tb = traceback.format_exc()
        print (tb)
        ser.close()
        time.sleep(5)

