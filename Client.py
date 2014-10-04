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
import time
import sys

logging.basicConfig(level=logging.INFO)

class Client():
	def __init__(self, api_url, ui_callback):
		self.api_url = api_url
		self.current_track = 0
		self.cookie = bytes("asdf", "UTF-8")
		self.collection = self.get_collection()
		self.playlist = []
		self.randomize_playlist()
		print(str(self.playlist))
		#sys.exit(0)
		self.playlist_length = int(self.collection[-1]["track_id"])
		logging.info("Collection length: %d" % (self.playlist_length))
		self.playing = False
		self.continous_playback = True
		self.player = Mpv(self.callback, ui_callback)
		self.cache = dict() # self.cache[str(track)] = dict()
							# self.cache[str(track)]["acc"] = time.time()
							# self.cache[str(track)]["filename"] = filename
		self.cache_strat = [-1, 0, 1, 2, 3]
		#threading.Thread(target=self.update_cache).start()
		self.update_cache()

	def randomize_playlist(self):
		self.playlist = []
		for i in self.collection:
			self.playlist.append(i["track_id"])
		return random.shuffle(self.playlist)
	
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
	
	def get_track(self, track):
		while str(track) not in self.cache:
			self.cache_track(track)
		self.cache[str(track)]["acc"] = time.time()
		return self.cache[str(track)]["filename"]
	
	def cache_track(self, track):
		if str(track) not in self.cache:
			api_string = self.api_url + "/get/track/" + str(track) + "/codec/opus/quality/128k"
			logging.info("Downloading %s" % (api_string))
			filename = self.download_file(api_string)
			self.cache[str(track)] = dict()
			self.cache[str(track)]["acc"] = time.time()
			self.cache[str(track)]["filename"] = filename
			logging.info("Cached %s" % (api_string))


	def toggle(self):
		if self.player.is_running():
			self.player.comm(" ")
			logging.info("Sent toggle")
			self.playing = not self.playing
		else:
			self.play(self.current_track)
			logging.info("Started playback")
	
	def _next(self):
		logging.info("Next track")
		self._stop()
		self.current_track += 1
		self.current_track %= len(self.playlist)
		self.play(self.current_track)
		self.update_cache()
	
	def skip(self):
		logging.info("Skipped track")
		if self.continous_playback:
			self._stop()
		else:
			self._next()
	
	def _stop(self):
		logging.info("_Stopping")
		self.player.comm("q")
		self.playing = False
	
	def stop(self):
		logging.info("Stopping")
		self.continous_playback = False
		self.player.comm("q")
		self.playing = False
	
	def play(self, track):
		self.continous_playback = True
		logging.info("Playing track %s" % (str(track)))
		self.current_track = track
		track = self.get_track(self.playlist[track])
		self.playing = True
		self.player.play(track)

	def update_cache(self):
		logging.info("Started cache update")
		for i in self.cache_strat:
			track = str(self.playlist[self.current_track+i])
			if track not in self.cache:
				self.cache_track(int(track))
		logging.info("inb4 while: %d > %d?" % (len(self.cache), len(self.cache_strat)))
		while len(self.cache) > len(self.cache_strat):
			logging.info("while: %d > %d" % (len(self.cache), len(self.cache_strat)))
			test = time.time()
			to_del = None
			for i in self.cache:
				if self.cache[i]["acc"] < test:
					to_del = i
					test = self.cache[i]["acc"]
			self.uncache(to_del)

	def uncache(self, track):
		logging.info("uncaching %s" % (track))
		to_del = self.cache[track]["filename"]
		os.remove(to_del)
		del self.cache[track]

	def clear_cache(self):
		for i in self.cache:
			os.remove(self.cache[i]["filename"])

	def callback(self):
		logging.info("callback called")
		if self.continous_playback:
			logging.info("continous playback")
			self._next()
