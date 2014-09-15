#!/usr/bin/python

import json
import logging
import os
import urllib.request
import threading
import subprocess
from tempfile import NamedTemporaryFile
from Player import Mpv
import random

API_URL = "http://localhost:8080/api"

logging.basicConfig(level=logging.INFO)

class Client():
	def __init__(self, api_url):
		self.api_url = api_url
		self.current_track = 1
		self.cookie = bytes("asdf", "UTF-8")
		self.collection = self.get_collection()
		self.playlist_length = int(self.collection[-1]["track_id"])
		logging.info("Collection length: %d" % (self.playlist_length))
		self.playing = False
		self.continous_playback = True
		self.player = Mpv(self.callback)
	
	def download_file(self, url):
		download = urllib.request.urlopen(url, data = self.cookie)
		f = NamedTemporaryFile(delete=False)
		f.write(download.read())
		f.close()
		return f.name
	
	def get_collection(self):
		collection = self.download_file(self.api_url + "/get/collection")
		fp = open(collection, "r")
		collection_dict = json.load(fp)
		fp.close()
		os.remove(collection)
		return collection_dict
	
	def display_collection(self):
		print(self.collection)
	
	def get_current_track(self):
		api_string = self.api_url + "/get/track/" + str(self.current_track) + "/codec/opus/quality/128k"
		logging.info("Downloading %s" % (api_string))
		return self.download_file(api_string)
	
	def get_rel_track(self, rel):
		tmp = self.current_track + rel
		if tmp < 0:
			tmp = (tmp + self.playlist_length)
		tmp %= (self.playlist_length + 1)
		return tmp
	
	def get_rand_track(self):
		return self.get_rel_track(random.randint(0, self.playlist_length))
	
	def cache(self):
		pass
	
	def toggle(self):
		if self.player.is_running():
			self.player.comm(" ")
			logging.info("Sent toggle")
			self.playing = not self.playing
		else:
			self.play()
			logging.info("Started playback")
	
	def next(self):
		logging.info("Next track")
		self._stop()
		self.play(self.get_rand_track())
	
	def skip(self):
		logging.info("Skipped track")
		if self.continous_playback:
			self._stop()
		else:
			self.next()
	
	def _stop(self):
		logging.info("_Stopping")
		self.player.comm("q")
		self.playing = False
	
	def stop(self):
		logging.info("Stopping")
		self.continous_playback = False
		self.player.comm("q")
		self.playing = False
	
	def play(self, track=0):
		self.continous_playback = True
		logging.info("Playing track %s" % (str(track)))
		self.playing = True
		if track != 0:
			self.current_track = track
		track = self.get_current_track()
		self.player.play(track)

	def callback(self):
		logging.info("callback called")
		if self.continous_playback:
			logging.info("continous playback")
			self.next()
	
	def start(self):
		self.playing = True
		while self.playing:
			if self.current_track == 0:
				self.current_track = 1
			track = self.get_current_track()
			logging.info("Starting playback")
			self.player.play(track)
			self.player.wait()
		#		if self.player.proc != None and self.player.proc.poll() == None:
		#			self.player.comm(command)
		#			logging.info("command is: %s" % (self.player.command))
			#self.current_track = self.get_rel_track(1)
			self.current_track = self.get_rand_track()
	
		
if __name__ == "__main__":
	client = Client(API_URL)
	client.display_collection()
	client.start()
