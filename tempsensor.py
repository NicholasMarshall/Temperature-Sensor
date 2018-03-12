import os
import glob
import time
import smtplib
import urllib.request
from w1thermsensor import W1ThermSensor


myAPI = "WPM8L7LQN0FXNJ82"
myDelay = 15 # how many seconds between posting data


def main():

    messageSent = False
    sensorNumber = "001"
    
    warningTemp = 72
    warningTempStr = str(warningTemp)

    print('starting...')

    baseURL = 'https://api.thingspeak.com/update?api_key={}'.format(myAPI)
    print(baseURL)
    sensor = W1ThermSensor()

    initialTempf = sensor.get_temperature(W1ThermSensor.DEGREES_F)
    initialTempfStr = str(initialTempf)

    senderEmail = "marshallmonitoring@gmail.com"
    targetEmail = "5593923611@mms.att.net"
    openingmsg = """Prototype Temperature sensor """ + sensorNumber +""" has been powered on.
    All sensor data alerts will be sent to this number. The current
    temperature of the sensor is: """ + initialTempfStr + "."

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, "Fresnostate1")

    server.sendmail(senderEmail, targetEmail, openingmsg)
    server.quit()


    while True:

        tempf = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        f = urllib.request.urlopen(baseURL +
                            "&field1={}".format(tempf))
            
        print(f.read())
        print(tempf)
        f.close()
        

        if tempf < warningTemp:
            if messageSent == False:
                senderEmail = "marshallmonitoring@gmail.com"
                targetEmail = "5593923611@mms.att.net"
                alertmsg = "Alert temperature is below  " + warningTempStr + " for sensor " + sensorNumber +"."

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(senderEmail, "Fresnostate1")

                server.sendmail(senderEmail, targetEmail, alertmsg)
                server.quit()

                messageSent = True
        if tempf > warningTemp:
            if messageSent == True:
                senderEmail = "marshallmonitoring@gmail.com"
                targetEmail = "5593923611@mms.att.net"
                alertmsg = "Alert temperature has risen above " + warningTempStr + " for sensor " + sensorNumber +"."

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(senderEmail, "Fresnostate1")

                server.sendmail(senderEmail, targetEmail, alertmsg)
                server.quit()

                messageSent = False
            

        time.sleep(int(myDelay))

main()
