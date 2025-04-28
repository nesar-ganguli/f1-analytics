import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="prores12345",
        database="driveToSurvive"
    )
