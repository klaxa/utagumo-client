#!/usr/bin/python

import logging
import os
import sys
import threading
from Player import Client

API_URL = "http://localhost:8080/api"

logging.basicConfig(level=logging.INFO)

class State():
	def __init__(self):
		self.playing = False

class Interface():
	
	def __init__(self):
		self.initUI()
		self.state = State()
		self.client = Client(API_URL)
	
	def toggle(self):
		self.client.toggle()
		self.update_state()
	
	def stop(self):
		self.client.stop()
		self.update_state()
	
	def next(self):
		self.client.skip()
		self.update_state()
	
	def get_status(self):
		return self.state
	
	def update_state(self):
		self.state.playing = self.client.playing
		self.refresh()
	
	def cleanup(self):
		self.client.stop()
	
	def refresh(self):
		pass
	
	def initUI(self):			   
		pass
