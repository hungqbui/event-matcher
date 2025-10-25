import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="eventmatcher"
)

def get_db_connection():
    return db

if __name__ == "__main__":
    if db.is_connected():
        print("Database connection successful")
    else:
        print("Failed to connect to database")