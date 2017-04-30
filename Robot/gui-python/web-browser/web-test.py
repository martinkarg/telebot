import webbrowser
import os

def PlaceCall():
	robot_login = "https://connection-robertoruano.c9users.io/robot_login.php?username=" + Robot_ID + "&pswrd=" + Robot_Password
	webbrowser.open_new_tab(robot_login)
	os.system("sudo su -c 'chromium-browser' -s /bin/sh pi")
	return robot_login

PlaceCall()