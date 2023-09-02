import wx
import sys
import application
import EasySpellchecker
from . import SecondaryScreen as sc
class window(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,parent=None,title="Easy Spellchecker")
		self.Centre()
		self.SetSize(wx.DisplaySize())
		#self.Maximize(True)
		panel=wx.Panel(self)
		menuBar=wx.MenuBar()
		mainMenu=wx.Menu()
		check=mainMenu.Append(-1,"Check the spelling of a word\tCTRL+S")
		quit=mainMenu.Append(-1,"Exit\tCTRL+Q")
		table=wx.AcceleratorTable([
			(wx.ACCEL_CTRL, ord("S"), check.GetId()),
			(wx.ACCEL_CTRL, ord("Q"), quit.GetId())
		])
		self.SetAcceleratorTable(table)
		menuBar.Append(mainMenu,"Main menu")
		about=wx.Menu()
		help=about.Append(-1,"Quick help\tF1")
		info=about.Append(-1,"About the program")
		menuBar.Append(about,"Help")
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU,lambda event: sc.dialog(self),check)
		self.Bind(wx.EVT_MENU,self.onQuit, quit)
		self.Bind(wx.EVT_MENU,self.onHelp,help)
		self.Bind(wx.EVT_MENU,self.onInfo,info)
		self.Bind(wx.EVT_CHAR_HOOK,self.onHook)
		self.Show()
		self.Raise()
		panel.SetFocus()
	def onQuit(self,event):
		self.Destroy()
		sys.exit()
	def onHelp(self,event):
		wx.MessageBox(application.quickhelp,"Information")
	def onInfo(self,event):
		wx.MessageBox(application.description,"Description")
	def onHook(self,event):
		if event.KeyCode==wx.WXK_F1:
			wx.MessageBox(application.quickhelp,"information")
			return
		elif event.KeyCode==wx.WXK_ESCAPE:
			self.Hide()
			EasySpellchecker.main()
			return
		else:
			event.Skip()