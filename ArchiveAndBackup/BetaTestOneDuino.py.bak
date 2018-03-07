# -*- coding: utf-8 -*-
import serial
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import traceback

###Variables:
ser = serial.Serial('/dev/ttyACM0',9600,timeout =10)
#ser2 = serial.Serial('/dev/ttyACM1',9600,timeout =10)
emailPassword = "Ilikepl@nts1"
#this is not very secure and in theory should be changed
toAddrGlobal = 'besae001@mail.goucher.edu'
alreadySentF = 0
alreadySentT = 0
alreadySentL = 0
alreadySentE = 0
alreadySentP = 0
alreadySentD = 0

count = 0
count2 = 0

maxFlow = 99999
minFlow = 15
minTemp = 40
maxTemp = 80
minLevel = 3
maxLevel = 8
minPH = 5.5
maxPH = 9.5
minEC = 15000
maxEC = 35000
minDO = 7
maxDO = 99999
#boolean highLow


###Functions


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

def levelCheck(levelVal):
    global alreadySentL
    if (levelVal>maxLevel or levelVal<minLevel):
        if(alreadySentL == 0 and count > 2):
            print('Your temp is out of Range! \n')
            sendLevelMail(levelVal)
            alreadySentL = 1
    if(levelVal<(maxLevel-.75) and levelVal>(minLevel+.75) and alreadySentL == 1):
        alreadySentL = 0
#--------------------
def PHCheck(phVal):
    global alreadySentP
    if (phVal>maxPH or phVal<minPH):
        if(alreadySentP == 0 and count2 > 2):
            print('Your PH is out of Range! \n')
            sendPHMail(phVal)
            alreadySentP = 1
    if(phVal<(maxPH-.75) and phVal>(minPH+.75) and alreadySentP == 1):
        alreadySentP = 0

def ECCheck(ECVal):
    global alreadySentE
    if (ECVal>maxEC or ECVal<minEC):
        if(alreadySentE == 0 and count2 > 2):
            print('Your EC is out of Range! \n')
            sendECMail(ECVal)
            alreadySentE = 1
    if(ECVal<(maxEC-5000) and ECVal>(minEC+5000) and alreadySentE == 1):
        alreadySentE = 0

def DOCheck(DOVal):
    global alreadySentD
    if (DOVal>maxDO or DOVal<minDO):
        if(alreadySentD == 0 and count2 > 2):
            print('Your DO is out of Range! \n')
            sendDOMail(DOVal)
            alreadySentD = 1
    if(DOVal<(maxDO-3) and DOVal>(minDO+3) and alreadySentD == 1):
        alreadySentD = 0

def sendTempMail(temp):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Temp out of Range"
    body = "Your water temp is out of range! Most recent reading is: " + str(temp) + "deg F. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()


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
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendLevelMail(waterLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Flow out of Range"
    body = "Your water level is out of range! Most recent reading is: " + str(waterLevel) + "in. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendDOMail(DOLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Dissolved O2 out of Range"
    body = "Your DO level is out of range! Most recent reading is: " + str(DOLevel) + "ppm. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendECMail(ECLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Electroconductivity out of Range"
    body = "Your EC level is out of range! Most recent reading is: " + str(ECLevel) + "uS/m. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendPHMail(PHLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = "besae001@mail.goucher.edu"
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: pH out of Range"
    body = "Your pH level is out of range! Most recent reading is: " + str(PHLevel) + "pH. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, "Ilikepl@nts1")
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
            val = val.lstrip(idVal) #see below comment.			print ('stripped Fval is ' + val)
            flowVal = float(val)
            flowCheck(flowVal)
            print ("Flow is " + str(flowVal))
	elif(idVal is 't'):
            val = val.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Tval is ' + val)
            tempVal = float(val)
            tempCheck(tempVal)
            print ("Temp is " + str(tempVal))
	elif(idVal is 'l'):
            val = val.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Lval is ' + val)
            levelVal = float(val)
            levelCheck(levelVal)
            print ("Temp is " + str(tempVal))
        count += 1
		
	"""	val2 = ser2.readline()
 	print ("Input value is: " + str(val2))
        stringList = []
        stringList.append(str(val2))
        idVal = stringList[0][:1]
        print ("id tag is " + str(idVal))
	if(idVal is 'p'):
            val2 = val2.lstrip(idVal) #see below comment.
            print ('stripped Pval is ' + val2)
            phVal = float(val2)
            PHCheck(phVal)
            print ("pH is " + str(phVal))
        elif(idVal is 'd'):
            val2 = val2.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Dval is ' + val2)
            doVal = float(val2)
            DOCheck(doVal)
            print ("Dissolved O2 is " + str(tempVal))
        elif(idVal is 'e'):
            val2 = val2.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Eval is ' + val2)
            ECVal = float(val2)
            ECCheck(ECVal)
            print ("EC is " + str(ECVal))
	count2 += 1
	"""
    except:
        print ("Wating for Device")
        tb = traceback.format_exc()
        print (tb)
        ser.close()
        time.sleep(5)



