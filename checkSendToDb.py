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

ser = "ABCD" # ttyACM1 for Arduino board
cursor = mydb.cursor()
value = (ser,'123')
query = "INSERT INTO timbangan (inputan,sensor) VALUES (%s,%s)"
cursor.execute(query,value)
print("Inserted",cursor.rowcount,"row(s) of data.")
mydb.commit()