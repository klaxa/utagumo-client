#!/usr/bin/python

import logging
import sys
from Client import Client
from Interface import Interface, State
from PyQt4 import QtGui, QtCore

API_URL = "http://localhost:8080/api"

logging.basicConfig(level=logging.INFO)

class UI(QtGui.QWidget, Interface):
	
	def __init__(self):
		super(UI, self).__init__()
		self.initUI()
		self.state = State()
		self.client = Client(API_URL, self.update_state)
	
	def refresh(self):
		#logging.info("State: %s %s/%s" % (str(self.state.playing), str(self.state.play_time), str(self.state.track_time)))
		if self.state.playing:
			self.togglebtn.setText("❚❚")
		else:
			self.togglebtn.setText("▶")
		self.play_time = str(self.state.play_time)
		self.track_time = str(self.state.track_time)
		self.time_label.setText(self.state.time_string)
	
	def initUI(self):
		
		hbox = QtGui.QHBoxLayout()
		vbox = QtGui.QVBoxLayout()
		
		#self.qbtn = QtGui.QPushButton('Quit', self)
		#self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		#self.qbtn.resize(self.qbtn.sizeHint())
		#hbox.addWidget(self.qbtn)
		
		self.togglebtn = QtGui.QPushButton('▶', self)
		self.togglebtn.clicked.connect(self.toggle)
		self.togglebtn.resize(self.togglebtn.sizeHint())
		
		hbox.addWidget(self.togglebtn)
		
		self.stopbtn = QtGui.QPushButton('◼', self)
		self.stopbtn.clicked.connect(self.stop)
		self.stopbtn.resize(self.stopbtn.sizeHint())
		
		hbox.addWidget(self.stopbtn)
		
		self.nextbtn = QtGui.QPushButton('▶❚', self)
		self.nextbtn.clicked.connect(self.next)
		self.nextbtn.resize(self.nextbtn.sizeHint())
		
		hbox.addWidget(self.nextbtn)
		vbox.addLayout(hbox)
		
		self.time_label = QtGui.QLabel("")
		self.time_label.resize(self.time_label.sizeHint())
		vbox.addWidget(self.time_label)
		self.setLayout(vbox)
		self.setWindowTitle('Utagumo client')	
		self.setGeometry(300, 300, 250, 10)
		self.show()


def main():
	app = QtGui.QApplication(sys.argv)
	ui = UI()
	app.aboutToQuit.connect(ui.cleanup)
	ret = app.exec_()
	#sys.exit(ret)



if __name__ == "__main__":
	main()
#	client = Client("http://localhost:8080/api")
#	client.display_collection()
#	client.start()
