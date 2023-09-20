from botocore.exceptions import ClientError
import boto3


class SQS:
	"""
	A class to interact with an SQS (Simple Queue Service) queue.
	"""

	def __init__(self):
		"""
		Initializes an SQS client and sets the queue URL.
		"""
		# URL of the SQS queue
		self.sqs_queue_url = "http://host.docker.internal:4566/000000000000/login-queue"

		# Initialize the boto3 SQS client
		self.sqs = boto3.client(
			"sqs",
			endpoint_url="http://host.docker.internal:4566",
			region_name="us-east-1"
		)

	def read_messages(self, limit: int = 100) -> list:
		"""
		Reads and returns messages from the SQS queue up to the specified limit.

		Parameters:
			limit (int): Maximum number of messages to read from the queue.

		Returns:
			list: List of messages read from the queue.
		"""
		# Initialize an empty list to store messages
		messages = []

		try:
			# Request messages from the SQS queue
			response = self.sqs.receive_message(
				QueueUrl=self.sqs_queue_url,
				MaxNumberOfMessages=limit
			)

			# Check if the response contains any messages
			if "Messages" in response:
				messages = response["Messages"]

				# Delete each message from the queue after it's read
				for message in messages:
					self._delete_message(message["ReceiptHandle"])

		except ClientError as e:
			# Log any errors that occur while reading messages
			print(f"Error reading messages from SQS: {e}")

		return messages

	def _delete_message(self, receipt_handle: str):
		"""
		Deletes a message from the SQS queue.

		Parameters:
			receipt_handle (str): The receipt handle of the message to be deleted.
		"""
		try:
			# Delete the message from the queue
			self.sqs.delete_message(
				QueueUrl=self.sqs_queue_url,
				ReceiptHandle=receipt_handle
			)
		except ClientError as e:
			# Log any errors that occur while deleting the message
			print(f"Error deleting message from SQS: {e}")
