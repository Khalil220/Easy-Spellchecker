import wx
from Functions.spellcheck import speller
class dialog(wx.Dialog):
	def __init__(self,parent):
		wx.Dialog.__init__(self,parent,title="Check a word")
		self.Center()
		self.SetSize(wx.DisplaySize())
		self.Maximize(True)
		self.panel=wx.Panel(self)
		self.choices=[]
		input=wx.StaticText(self.panel,-1,"&Type the word here",name="userInput")
		self.uinput=wx.TextCtrl(self.panel,-1,name="userInput")
		self.uinput.SetFocus()
		self.checkbutton=wx.Button(self.panel,-1,"Check",name="userInput")
		self.checkbutton.SetDefault()
		self.rt=wx.StaticText(self.panel,-1,"Co&rrection",name="output")
		self.outputOne=wx.TextCtrl(self.panel,-1,style=wx.TE_READONLY|wx.TE_RICH|wx.TE_MULTILINE|wx.HSCROLL,name="output")
		self.quit=wx.Button(self.panel,wx.ID_CANCEL,"&close",name="exit")
		self.checkbutton.Bind(wx.EVT_BUTTON,self.onCheck)
		self.quit.Bind(wx.EVT_BUTTON,self.onQuit)
		sizer=wx.BoxSizer(wx.VERTICAL)
		sizerOne=wx.BoxSizer(wx.HORIZONTAL)
		sizerTwo=wx.BoxSizer(wx.HORIZONTAL)
		sizerThree=wx.BoxSizer(wx.HORIZONTAL)
		for i in self.panel.GetChildren():
			if i.Name=="userInput":
				sizerOne.Add(i,0)
			elif i.Name=="output":
				sizerTwo.Add(i,1,wx.ALL)
				i.Show(False)
			elif i.Name=="exit":
				sizerThree.Add(i,1)
		sizer.Add(sizerOne,1,wx.EXPAND)
		sizer.Add(sizerTwo,1,wx.EXPAND)
		sizer.Add(sizerThree,1,wx.EXPAND)
		self.panel.SetSizer(sizer)
		self.speller=speller()
		self.ShowModal()
	def onCheck(self,event):
		value=self.uinput.GetValue()
		correction=self.speller(value)
		self.outputOne.Clear()
		self.outputOne.AppendText(correction)
		for i in self.panel.GetChildren():
			if i.Name=="output" and not i.Show():
				i.Show()
		self.outputOne.SetFocus()
	def onQuit(self,event):
		self.Destroy()