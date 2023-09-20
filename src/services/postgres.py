from abc import ABC, abstractmethod
from typing import List, Any


class Postgres(ABC):
	"""
	Abstract base class for Postgres-related operations.
	"""

	def get_records(self, wrappers: List[Any]) -> List[Any]:
		"""
		Retrieves records from a list of wrapper objects.

		Parameters:
			wrappers (List[Any]): List of wrapper objects that contain records.

		Returns:
			List[Any]: List of records retrieved from wrapper objects.
		"""
		# Initialize an empty list to store records
		records = []

		# Loop through each wrapper object to get records
		for wrapper in wrappers:
			records.append(wrapper.get_record())

		return records

	@abstractmethod
	def get_insert_query(self) -> str:
		"""
		Abstract method to get the SQL insert query.

		Returns:
			str: SQL insert query as a string.
		"""
		pass

	@abstractmethod
	def insert(self, records: List[Any]) -> None:
		"""
		Abstract method to insert records into the Postgres database.

		Parameters:
			records (List[Any]): List of records to insert into the database.
		"""
		pass
