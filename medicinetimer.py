import mysql.connector
import requests
import datetime

NOTIFICATION_INTERVAL = 5.0 #Notification interval in minutes
EVENT_NAME = "medicine_timer"
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/{}/with/key/{}"

#Connect to database
dbReadConnection = mysql.connector.connect(
    host="localhost",
    user="Script_MedicineTimer",
    passwd="3fP@d22q",
    database='Medicine_Timer'
)
dbWriteConnection = mysql.connector.connect(
    host="localhost",
    user="Script_MedicineTimer",
    passwd="3fP@d22q",
    database='Medicine_Timer',
    autocommit=True
)
readCursor = dbReadConnection.cursor()

query = ("Call sp_GetExpiredTimers")

readCursor.execute(query)

#Iterate through returned data
for (userID, timerName, webhook, exceededTimer, lastNotified) in readCursor:
    #lastNotifiedTime = datetime.datetime.strptime(lastNotified, "%Y-%m-%d %H:%M:%S") #convert string to datetime
    timeDiff = datetime.datetime.now() - lastNotified
    if (timeDiff > datetime.timedelta(minutes=NOTIFICATION_INTERVAL)): #Timer is due to be notified
        if (exceededTimer):
            message = 'Timer {} is overdue; please take it now!'.format(timerName)
        else:
            message = 'Time to take {}!'.format(timerName)
        data = {'value1': message, 'value2' : 'https://www.google.com'}
        webhookURL = IFTTT_WEBHOOK_URL.format(EVENT_NAME, webhook)
        requests.post(webhookURL, json=data)
        query = "Call sp_SetNotificationTime({})".format(userID)
        writeCursor = dbWriteConnection.cursor()
        writeCursor.execute(query)
        writeCursor.close()
readCursor.close()
dbReadConnection.close()
dbWriteConnection.close()
