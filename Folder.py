import sys
import os
import uuid
import queue
import glob

# This class represents simple queue using a folder
class Queue(queue.Queue):
	def __init__(self, config):
		super(Queue, self).__init__(config)
		if (not os.path.isdir(config["path"])): 
			sys.stderr.write("[Folder Queue Error] No such folder " + config["path"] + "\n")
			sys.exit(1)

	# enqueues a message into a queue
	def enqueue(self, message_body):
		message_file = open(self.config["path"] + "/" + str(uuid.uuid4()), 'w')
		message_file.write(message_body)
		message_file.close()

	# dequeues one message from a queue and returns message object
	def dequeue(self):
		files = filter( lambda f: not f.startswith('.'), os.listdir(self.config["path"] + "/"))
		if (len(files) == 0):
			return None

		filename = files[0];

		os.rename(self.config["path"] + "/" + filename, self.config["path"] + "/." + filename)

		message_file = open(self.config["path"] + "/." + filename, 'r')
		content = message_file.read()
		message_file.close()

		return Message(self, filename, content)

	def release_message(self, message):
		os.rename(self.config["path"] + "/." + message.filename, self.config["path"] + "/" + message.filename)

	def delete_message(self, message):
		os.remove(self.config["path"] + "/." + message.filename)

class Message(queue.Message):
	def __init__(self, queue, filename, content):
		super(Message, self).__init__(queue)
		self.filename = filename
		self.content = content

	def __repr__(self):
		return self.content
