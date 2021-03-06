#!/usr/bin/env python3

import logging
from Client import Client
from Interface import Interface, State
from tkinter import Tk, Frame, Button, FALSE

API_URL = "http://localhost:8080/api"
logging.basicConfig(level=logging.INFO)

class UtaGUI(Frame, Interface):
	def __init__(self, parent):
		self.parent = parent
		self.state = State()
		self.initUI()
		self.client = Client(API_URL)

	def refresh(self):
		logging.info("State: %s" % (str(self.state.playing)))
		if self.state.playing:
			self.playbtn["text"] = "❚❚"
		else:
			self.playbtn["text"] = "▶"

	def initUI(self):
		self.playbtn = Button(width="4", text="▶")
		self.playbtn["command"] = self.toggle

		self.stopbtn = Button(width="4", text="◼")
		self.stopbtn["command"] = self.stop

		self.nextbtn = Button(width="4", text="▶❚")
		self.nextbtn["command"] = self.next

		self.playbtn.grid(row=0, column=0, padx=10)
		self.stopbtn.grid(row=0, column=1, pady=10)
		self.nextbtn.grid(row=0, column=2, padx=10)

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

if __name__ == '__main__':
	main()
