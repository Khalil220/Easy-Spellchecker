import keyboard
import wx
import sys
import time
from threading import Thread
from GUI.MainScreen import window
from application import hotkey,notification
from Functions.notifier import notify
app=wx.App()
Thread(target=notify,args=["",notification,30],daemon=True).start()
def main():
	while 1:
		if keyboard.is_pressed(hotkey):
			break
		time.sleep(0.005)
	window()
	app.MainLoop()