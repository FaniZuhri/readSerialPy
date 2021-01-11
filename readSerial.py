import serial
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

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1) # ttyACM1 for Arduino board

readOut = 0   #chars waiting from laser range finder

print ("Starting up")
connected = False
commandToSend = 1 # get the distance in mm

sn = "2021010011"

while True:
    print ("Writing: ",  commandToSend)
    ser.write(str(commandToSend).encode())
    time.sleep(1)
    commandToSend += 1
    while True:
        try:
            print ("Attempt to Read")
            readOut = ser.readline().decode('utf-8')
            dataReceived = str(readOut)
            time.sleep(1)
            print ("Reading: ", dataReceived)

            if(dataReceived!=''):
                cursor = mydb.cursor()
                value = (sn,dataReceived)
                query = "INSERT INTO timbangan (sn,value) VALUES (%s,%s)"
                cursor.execute(query,value)
                print("Inserted",cursor.rowcount,"row(s) of data.")
                mydb.commit()
                data = {'sn': sn,
                        'value': dataReceived,
                        }
                post =requests.get('http://smart-gh.com/inputt.php?sn=2021010011', params=data)
                if post.status_code == 200:
                    print('Data Weightbridge has been sent to Database Server')
                elif post.status_code == 404:
                    print('Not Found. \n')
                elif post.status_code == 500:
                    print('Failed \n')
            break
        except:
            pass
    print ("Restart")
    ser.flush() #flush the buffer