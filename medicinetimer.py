import mysql.connector

dbConnection = mysql.connector.connect(
    host="localhost",
    user="Script_MedicineTimer",
    passwd="3fP@d22q",
    database='Medicine_Timer'
)

print(dbConnection)