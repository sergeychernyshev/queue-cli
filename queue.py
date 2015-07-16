from abc import ABCMeta, abstractmethod
import sys
import ConfigParser

# Generic class representing a queue, to be subclassed by specific implementations
class Queue(object):
	__metaclass__ = ABCMeta

	# all queues will be initialized by passing a collection of name/value pairs
	def __init__(self, config):
		self.config = config

	# enqueues a message into a queue
	@abstractmethod
	def enqueue(self, message_body):
		pass # abstract, implement your own

	# dequeues one message from a queue and returns message object
	@abstractmethod
	def dequeue(self):
		return false # abstract, implement your own

	# releases message back to the queue
	@abstractmethod
	def release_message(self, message):
		pass # abstract, implement your own

	# deletes message from the queue
	@abstractmethod
	def delete_message(self, message):
		pass # abstract, implement your own

	# returns queue statistics
	@abstractmethod
	def stats(self):
		pass # abstract, implement your own

class Message(object):
	__metaclass__ = ABCMeta

	# simple message with just a body, you most likely want to override it 
	def __init__(self, queue):
		self.queue = queue

	# all messages must overrid __repr__() method to return body of the message
	@abstractmethod
	def __repr__(self):
		return "Implement this" 

	# releases message back to the queue
	def release(self):
		self.queue.release_message(self)

	# delete message from the queue
	def delete(self):
		self.queue.delete_message(self)

def get(config_file, queue_name):
	# Read configuration files to see if
	from ConfigParser import SafeConfigParser
	parser = SafeConfigParser()
	parser.read(config_file)

	try:
	    config_pairs = parser.items(queue_name)
	except ConfigParser.NoSectionError:
	    sys.stderr.write("No such queue defined: " + queue_name + "\n")
	    sys.exit(1)

	config = {}
	for name, value in config_pairs:
	    config[name] = value

	module = __import__(config["type"])
	return getattr(module, 'Queue')(config)
