import queue
import boto.sqs

# This class represents Amazon Web Services SQS queue
class Queue(queue.Queue):
	def __init__(self, config):
		super(Queue, self).__init__(config)
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

		return Message(self, aws_messages[0])

	def release_message(self, message):
		message.aws_message.change_visibility(0)

	def delete_message(self, message):
		self.aws_queue.delete_message(message.aws_message)	

class Message(queue.Message):
	def __init__(self, queue, aws_message):
		super(Message, self).__init__(queue)
		self.aws_message = aws_message

	def __repr__(self):
		return self.aws_message.get_body()
