# -*- coding: utf-8 -*-
import serial
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import traceback

import sqlite3
from sqlite3 import Error


###Variables:
ser = serial.Serial('/dev/ttyACM0',9600,timeout =10)
#ser2 = serial.Serial('/dev/ttyACM1',9600,timeout =10)
emailPassword = "Ilikepl@nts1"
#this is not very secure and in theory should be changed
toAddr= 'besae001@mail.goucher.edu'

database = '/var/www/db/greenhouse.db'
#database = '~pi/GreenHouseFiles/Working/greenhouse.db'
#database = 'greenhouse.db'

#used to prevent multiple sends of alert emails
alreadySentF = 0
alreadySentT = 0
alreadySentL = 0
alreadySentE = 0
alreadySentP = 0
alreadySentD = 0

count = 0
count2 = 0

#used to keep track of how often readings re stored to database
fCount = 0
tCount = 0
lCount = 0
eCount = 0
pCount = 0
dCount = 0

maxFlow = 99999
minFlow = 15
minTemp = 40
maxTemp = 80
minLevel = 3
maxLevel = 9
minPH = 5.5
maxPH = 9.5
minEC = 15000
maxEC = 35000
minDO = 7
maxDO = 99999
#boolean highLow


###Functions

def create_connection(db_file):
#create a database connection to SQLite db
    try:
	print "create_connection to ", db_file
        conn = sqlite3.connect(db_file)
	print "Connected to ", str(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def insert_reading(con, reading):
    print "Inserting reading; con = %s, reading = %s" %(con, reading)
    if not con:
	global database
	print "Retrying to connect to database"
	con = create_connection(database)
    sql = ' INSERT INTO reading (date, time, reading, sensorID) values (?,?,?,?)' 
    cur = con.cursor()
    cur.execute(sql, reading) #reading structure is ( date, time, reading, 'ID')
    con.commit()
    return cur.lastrowid


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
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    global emailPassword
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Temp out of Range"
    body = "Your water temp is out of range! Most recent reading is: " + str(temp) + "deg F. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()


def sendFlowMail(flow):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    global emailPassword
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Flow out of Range"
    body = "Your water flow is out of range! Most recent reading is: " + str(flow) + "L/s. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendLevelMail(waterLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp
    global emailPassword
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Flow out of Range"
    body = "Your water level is out of range! Most recent reading is: " + str(waterLevel) + "in. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendDOMail(DOLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp
    
    global emailPassword
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Dissolved O2 out of Range"
    body = "Your DO level is out of range! Most recent reading is: " + str(DOLevel) + "ppm. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendECMail(ECLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    global emailPassword
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: Electroconductivity out of Range"
    body = "Your EC level is out of range! Most recent reading is: " + str(ECLevel) + "uS/m. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()

def sendPHMail(PHLevel):

#can add in a highLow parameter to print the flow is too high or too low rather than just the flow is out of range
#maybe add a time stamp

    global emailPassword
    global toAddr
    fromAddress = "GoucherGreenhouseMonitor@gmail.com"
    toAddress = toAddr
    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "GREENHOUSE ALERT: pH out of Range"
    body = "Your pH level is out of range! Most recent reading is: " + str(PHLevel) + "pH. Please address this immediately \n \n Thank you, \n Greenhouse Monitoring System"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, emailPassword)
    message = msg.as_string()
    server.sendmail(fromAddress, toAddress, message)
    server.quit()
###Main


"""Database"""

conn = create_connection(database)

"""Sensors"""

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
            fCount += 1
	    if fCount == 50:
                reading = (str(datetime.date.today()),time.strftime("%H:%M:%S"),flowVal,'FL')
                insert_reading(conn,reading)
		fCount = 0
            print ("Flow is " + str(flowVal))
	elif(idVal is 't'):
            val = val.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Tval is ' + val)
            tempVal = float(val)
            tempCheck(tempVal)
            tCount += 1
	    if tCount == 50:
                reading = (str(datetime.date.today()),time.strftime("%H:%M:%S"),tempVal,'TP')
                insert_reading(conn,reading)
		tCount = 0
            print ("Temp is " + str(tempVal))
	elif(idVal is 'l'):
            val = val.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Lval is ' + val)
            levelVal = float(val)
            levelCheck(levelVal)
            lCount += 1
	    if lCount == 50:
                reading = (str(datetime.date.today()),time.strftime("%H:%M:%S"),levelVal,'WL')
                insert_reading(conn,reading)
		lCount = 0
            print ("Level is " + str(levelVal))
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
            reading = (datetime.datetime.now.strptime("%y%m%d"),datetime.datetime.now.strptime("%H%M%S"),str(phVal),'PH')
            insert_reading(conn,reading)
            print ("pH is " + str(phVal))
        elif(idVal is 'd'):
            val2 = val2.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Dval is ' + val2)
            doVal = float(val2)
            DOCheck(doVal)
            reading = (datetime.datetime.now.strptime("%y%m%d"),datetime.datetime.now.strptime("%H%M%S"),str(doVal),'DO')
            insert_reading(conn,reading)
            print ("Dissolved O2 is " + str(tempVal))
        elif(idVal is 'e'):
            val2 = val2.lstrip(idVal) #the doc for lstrip says (s[,chars]) so this might error
            print ('stripped Eval is ' + val2)
            ECVal = float(val2)
            ECCheck(ECVal)
            reading = (datetime.datetime.now.stpftime("%y%m%d"),datetime.datetime.now.strptime("%H%M%S"),str(ECVal),'EC')
            insert_reading(conn,reading)
            print ("EC is " + str(ECVal))
	count2 += 1
	"""
    except:
        print ("Wating for Device")
        tb = traceback.format_exc()
        print (tb)
        ser.close()
        time.sleep(5)



###UPDATE LOG
"""	5/4/17 - made toAddr and emailPassword globals
	5/4/17 - added database functionality including 'reading' value in all of the elifs
        5/4/17 - added UPDATE LOG to bottom of document
	5/9/17 - fixed connection to database
	5/9/17 - updated insert queries

"""
