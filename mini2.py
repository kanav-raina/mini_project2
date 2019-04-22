import RPi.GPIO as GPIO
import time
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from threading import *

class Parent:

   def camera(self):
      subprocess.check_output(['/home/pi/Desktop/mini_project2/file.sh'])

   def buzzer(self):    
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(5,GPIO.OUT)
      GPIO.output(5, GPIO.HIGH)
      time.sleep(5)
      GPIO.output(5,GPIO.LOW)
   
   def sendmail(self,message):
      fromaddr = "kanavraina98@gmail.com"
      toaddr = "16bcs020@smvdu.ac.in"
      msg = MIMEMultipart() 
      msg['From'] = "kanavraina98@gmail.com"
      msg['To'] = "16bcs020@smvdu.ac.in"
      msg['Subject'] = "Home Security System"
      body =  message
      msg.attach(MIMEText(body, 'plain'))
      filename = "image.jpg"
      attachment = open("/home/pi/Desktop/mini_project2/image.jpg", "rb")
      p = MIMEBase('application', 'octet-stream')
      p.set_payload((attachment).read()) 
      encoders.encode_base64(p) 
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
      msg.attach(p)
      s = smtplib.SMTP('smtp.gmail.com', 587) 
      s.ehlo()
      s.starttls() 
      password='ENTER YOUR PASSWORD HERE IN BASE64 ENCODED FORMAT'.decode("base64")
      s.login(fromaddr, password) 
      text = msg.as_string()
      s.sendmail(fromaddr, toaddr, text)
      s.quit()
	
class IR(Parent,Thread):
   def run(self):
      global dead
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(2,GPIO.IN)
      while (not dead):
        i=GPIO.input(2)
        if(i==0):
           print("no interrupt",i)
           time.sleep(1)
        elif(i==1):
           print("Motion Detected in your house ") 
           self.buzzer()
           self.camera()
           self.sendmail("Motion Detected in your house") 
           print("Email Sent")
           continue

class Gas(Parent,Thread):
   def run(self):
      global dead
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(26,GPIO.IN)
      while (not dead): 
         i=GPIO.input(26)
         if(i==1):
            print("No gas leakage detected")
            time.sleep(1)
         elif(i==0):
            test=1
            print("GAS DETECTED")
            self.buzzer()
            self.camera()
            self.sendmail("Gas Leakage detected in your house")
            print("Email Sent")
            continue


global dead
dead=False
i=IR()

i.start()
g=Gas()
g.start()
raw_input("Press enter to disable sensors")
while(True):
	pwd=raw_input(" Enter password  to disable sensors: ")
	if(pwd=="disable"):
		dead=True
		break
	else:
		print("Wrong Password")
		raw_input("press enter to disable sensors")
		continue
