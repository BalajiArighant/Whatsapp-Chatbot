from rest_framework.response import Response
from rest_framework.views import APIView
import psycopg2
from dotenv import load_dotenv, find_dotenv
import os

class HelloWorld(APIView):
	def get(self, request):
		load_dotenv(find_dotenv())
		USER = os.getenv("DB_USER")
		PASSWORD = os.getenv("DB_PASSWORD")
		HOST = os.getenv("DB_HOST")
		PORT = os.getenv("DB_PORT")
		DBNAME = os.getenv("DB_NAME")

		# Connect to the database
		try:
			connection = psycopg2.connect(
				user=USER,
				password=PASSWORD,
				host=HOST,
				port=PORT,
				dbname=DBNAME
			)
			print("Connection successful!")
			
			# Create a cursor to execute SQL queries
			cursor = connection.cursor()
			
			# Example query
			cursor.execute("SELECT NOW();")
			result = cursor.fetchone()
			print("Current Time:", result)

			# Close the cursor and connection
			cursor.close()
			connection.close()
			print("Connection closed.")
			return Response({"message": {"Current Time": result}})

		except Exception as e:
			print(f"Failed to connect: {e}")
			return Response({"message": "Failed to connect to the database."})