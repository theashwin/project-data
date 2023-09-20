import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List

import psycopg2
from psycopg2.extras import execute_values
from dataclasses import dataclass, field
from services.postgres import Postgres


@dataclass
class UserLoginWrapper:
	"""
	A wrapper for user login data, with fields automatically hashed where necessary.
	"""
	user_id: str
	device_type: str
	masked_ip: str
	masked_device_id: str
	locale: str
	app_version: int
	create_date: str = field(default_factory=lambda: datetime.now().isoformat())

	def __post_init__(self):
		"""
		Post-initialization to hash sensitive fields.
		"""
		self.masked_ip = self.mask(self.masked_ip)
		self.masked_device_id = self.mask(self.masked_device_id)

	def mask(self, unmasked: str) -> str:
		"""
		Hashes a string using SHA-256.

		Parameters:
			unmasked (str): The string to hash.

		Returns:
			str: The hashed string.
		"""
		return hashlib.sha256(unmasked.encode("utf-8")).hexdigest()

	def get_record(self) -> tuple:
		"""
		Returns the record as a tuple.

		Returns:
			tuple: The record as a tuple.
		"""
		return (
			self.user_id,
			self.device_type,
			self.masked_ip,
			self.masked_device_id,
			self.locale,
			self.app_version,
			self.create_date
		)


def create_record(data: Dict[str, Any]) -> Optional[UserLoginWrapper]:
	"""
	Creates a UserLoginWrapper record from a dictionary of data.

	Parameters:
		data (Dict[str, Any]): The data to create a record from.

	Returns:
		Optional[UserLoginWrapper]: The created record or None if data is None.
	"""
	if data is None:
		return None

	# If all the keys are not present then the data is considered incomplete and thus discarded.
	if not data.get("user_id") and not data.get("device_type") and not data.get("ip") and not data.get("device_id") \
			and not data.get("locale") and not data.get("app_version"):
		return None

	return UserLoginWrapper(
		user_id=data.get("user_id", ""),
		device_type=data.get("device_type", ""),
		masked_ip=data.get("ip", ""),
		masked_device_id=data.get("device_id", ""),
		locale=data.get("locale", ""),
		app_version=int(data.get("app_version", "0").replace(".", ""))
	)


class UserLogins(Postgres):
	"""
	Handles database operations related to user logins.
	"""

	def __init__(self):
		"""
		Initializes the database connection parameters.
		"""
		self.connection = {
			"dbname": "postgres",
			"user": "postgres",
			"password": "postgres",
			"host": "host.docker.internal",
			"port": 5432,
		}

	def get_insert_query(self) -> str:
		"""
		Constructs the SQL query for inserting records into the user_logins table.

		Returns:
			str: SQL query string for insertion.
		"""
		return """
            INSERT INTO user_logins (
                user_id,
                device_type,
                masked_ip,
                masked_device_id,
                locale,
                app_version,
                create_date
            ) VALUES %s;
        """

	def insert(self, records: List[UserLoginWrapper]) -> None:
		"""
		Inserts a list of records into the database.

		Parameters:
			records (List[UserLoginWrapper]): List of records to insert.
		"""
		insert_query = self.get_insert_query()

		with psycopg2.connect(**self.connection) as conn:
			with conn.cursor() as cur:
				# Convert the UserLoginWrapper objects to tuples
				converted_records = self.get_records(records)

				# Log the records being inserted for debugging
				print(f"Inserting records: {converted_records}")

				# Execute the insert query
				execute_values(cur, insert_query, converted_records)

			# Commit the transaction to save changes
			conn.commit()
