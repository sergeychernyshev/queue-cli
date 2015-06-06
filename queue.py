from abc import ABCMeta, abstractmethod
import boto.sqs
import sys
import subprocess 
import ConfigParser
import getopt 

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

# This class represents Amazon Web Services SQS queue
class SQS(Queue):
	def __init__(self, config):
		super(SQS, self).__init__(config)
		self.aws_conn = boto.sqs.connect_to_region(self.config["region"])
		self.aws_queue = self.aws_conn.get_queue(self.config["queue"])

	# enqueues a message into a queue
	def enqueue(self, message_body):
		aws_message = boto.sqs.message.RawMessage()
		aws_message.set_body(message_body)
		self.aws_queue.write(aws_message)

	# dequeues one message from a queue and returns message object
	def dequeue(self):
		aws_messages = self.aws_queue.get_messages(1)
		if (len(aws_messages) == 0):
			return None

		return SQSMessage(self, aws_messages[0])

	def release_message(self, message):
		message.aws_message.change_visibility(0)

	def delete_message(self, message):
		self.aws_queue.delete_message(message.aws_message)	

class SQSMessage(Message):
	def __init__(self, queue, aws_message):
		super(SQSMessage, self).__init__(queue)
		self.aws_message = aws_message

	def __repr__(self):
		return self.aws_message.get_body()
