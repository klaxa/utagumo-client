#!/usr/bin/env python3

import logging
from Player import Client
from Interface import Interface, State
from tkinter import Tk, Frame, Button, FALSE

API_URL = "http://dedi.klaxa.eu:8080/api"
logging.basicConfig(level=logging.INFO)

class UtaGUI(Frame, Interface):
	def __init__(self, parent):
		self.parent = parent
		self.state = State()
		self.initUI()
		self.client = Client(API_URL)

	def initUI(self):
		self.playbtn = Button(width="4", text="▶❚❚")
		self.playbtn["command"] = self.toggle

		self.stopbtn = Button(width="4", text="◼")
		self.stopbtn["command"] = self.stop

		self.nextbtn = Button(width="4", text="▶❚")
		self.nextbtn["command"] = self.next

		self.playbtn.pack()
		self.stopbtn.pack()
		self.nextbtn.pack()

		#self.playbtn.grid(row=0, column=0)
		#self.stopbtn.grid(row=0, column=1)
		#self.nextbtn.grid(row=0, column=2)

def main():
	root = Tk()

	root.title("Utagumo")
	root.resizable(width=FALSE, height=FALSE)
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	root.geometry('+%d+%d' % (ws/2, hs/2))

	app = UtaGUI(root)
	def shutdown():
		app.cleanup()
		root.destroy()
	root.protocol("WM_DELETE_WINDOW", shutdown)

	logging.info("Running")
	root.mainloop()
	logging.info("Dying")
	app.destroy()

if __name__ == '__main__':
	main()
