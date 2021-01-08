import serial
import time
import mysql.connector
import requests
import datetime
import time

mydb = mysql.connector.connect(
    host='localhost', #hostname
    user='root', #username
    passwd='', #password
    database='smartgh_pemantauan') #database name'
print(mydb)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1) # ttyACM1 for Arduino board

readOut = 0   #chars waiting from laser range finder

print ("Starting up")
connected = False
commandToSend = 1 # get the distance in mm

sn = "2020060001"

while True:
    print ("Writing: ",  commandToSend)
    ser.write(str(commandToSend).encode())
    time.sleep(1)
    while True:
        try:
            print ("Attempt to Read")
            readOut = ser.readline().decode('utf-8')
            dataReceived = str(readOut)
            time.sleep(1)
            print ("Reading: ", dataReceived)

            if(dataReceived!=''):
                print("abc")
                mycursor = mydb.cursor()
                sql ="INSERT INTO timbangan (inputan) VALUES (%s)"
                val = (dataReceived)
                mycursor.execute(sql, val)
                print(sql)
                print(val)
                mydb.commit()

                data = {'sn': sn,
                        'inputan': dataReceived,
                        }
                post =requests.get('http://smart-gh.com/input.php?sn=2020060001', params=data)
                if post.status_code == 200:
                    print('Data Monitoring has been sent to Database Server')
                elif post.status_code == 404:
                    print('Not Found. \n')
                elif post.status_code == 500:
                    print('Failed \n')
            break
        except:
            pass
    print ("Restart")
    ser.flush() #flush the buffer