# -*- coding: utf-8 -*-
import serial
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import traceback

###Variables:
ser = serial.Serial('/dev/ttyACM0',9600,timeout =10)
alreadySentF = 0
alreadySentT = 0
count = 0
maxFlow = 100
minFlow = 10
minTemp = 66
maxTemp = 77
#boolean highLow


###Functions


def sendFlowMail(flow):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Flow out of Range"
    body = "Your water flow is out of range! Most recent reading is: " + str(flow) + "L/s. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikeplants1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()
###FUNctions

def flowCheck(flowVal):
    global alreadySentF
    if (flowVal>maxFlow or flowVal<minFlow):
        if(alreadySentF == 0 and count > 2):
            print('Your flow is out of Range! \n')
            sendFlowMail(flowVal)
            alreadySentF = 1
    if(flowVal<(maxFlow-10) and flowVal>(minFlow+10) and alreadySentF == 1):
        alreadySentF = 0

def tempCheck(tempVal):
    global alreadySentT
    if (tempVal>maxTemp or tempVal<minTemp):
        if(alreadySentT == 0 and count > 2):
            print('Your temp is out of Range! \n')
            sendTempMail(tempVal)
            alreadySentT = 1
    if(tempVal<(maxTemp-2) and tempVal>(minTemp+2) and alreadySentT == 1):
        alreadySentT = 0

def sendTempMail(temp):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Temp out of Range"
    body = "Your water flow is out of range! Most recent reading is: " + str(temp) + "deg F. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

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
        print ("Input value is: " + str(val))
        stringList = []
        stringList.append(str(val))
        idVal = stringList[0][:1]
        print ("id tag is " + str(idVal))
	if(idVal is 'f'):
		val = val.lstrip(idVal) #see below comment.
		print ('stripped Fval is ' + val)
		flowVal = float(val)
		flowCheck(flowVal)
		print ("Flow is " + str(flowVal))
	elif(idVal is 't'):
		val = val.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
                print ('stripped Tval is ' + val)
		tempVal = float(val)
		tempCheck(tempVal)
                print ("Temp is " + str(tempVal))
        count += 1

	

    except:
        print ("Wating for Device")
        tb = traceback.format_exc()
        print (tb)
        ser.close()
        time.sleep(5)



