# import serial
import time
import mysql.connector
import requests
import datetime
import time

mydb = mysql.connector.connect(
    host='localhost', #hostname
    user='smartgh', #username
    passwd='**hydr0p0n1c##', #password
    database='smartgh_pemantauan') #database name'
# print(mydb)
sn = "2020060001"
ser = "ABCD" # ttyACM1 for Arduino board
cursor = mydb.cursor()
value = (sn,ser)
query = "INSERT INTO timbangan (sn,sensor) VALUES (%s,%s)"
cursor.execute(query,value)
print("Inserted",cursor.rowcount,"row(s) of data.")
mydb.commit()