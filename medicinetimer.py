import mysql.connector
import requests

#Connect to database
dbConnection = mysql.connector.connect(
    host="localhost",
    user="Script_MedicineTimer",
    passwd="3fP@d22q",
    database='Medicine_Timer'
)
cursor = dbConnection.cursor()

query = ("Call sp_GetExpiredTimers")

cursor.execute(query)

#Iterate through returned data
for (timerName, webhook, exceededTimer) in cursor:
    if (exceededTimer):
        print("Timer for {} is very overdue; sending to hook {}".format(timerName, webhook))
    else:
        print("Timer for {} is due; sending to hook {}".format(timerName, webhook))
