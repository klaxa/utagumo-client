#!/usr/bin/python

import logging
import os
import sys
import threading
import re
from Client import Client

API_URL = "http://localhost:8080/api"

logging.basicConfig(level=logging.INFO)

class State():
	def __init__(self):
		self.playing = False
		self.play_time = self._string_to_secs("00:00:00")
		self.track_time = self._string_to_secs("00:00:00")
		self.time_string = "00:00:00/00:00:00"
	def _string_to_secs(self, string):
		values = string.split(":")
		assert(len(values) == 3)
		return int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])

class Interface():
	
	def __init__(self):
		self.initUI()
		self.state = State()
		self.client = Client(API_URL, self.update_state)
	
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
		times = re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", self.client.player.stderr)
		if len(times) == 2:
			self.state.play_time = self.state._string_to_secs(times[0])
			self.state.track_time = self.state._string_to_secs(times[1])
			self.state.time_string = times[0] + "/" + times[1]
		self.refresh()
	
	def cleanup(self):
		self.client.stop()
		self.client.clear_cache()
	
	def refresh(self):
		pass
	
	def initUI(self):
		pass
