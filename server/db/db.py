import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="dev_user",
    password="Team15",
    database="eventmatcher"
)

def get_db_connection():
    return db

if __name__ == "__main__":
    if db.is_connected():
        print("Database connection successful")
    else:
        print("Failed to connect to database")