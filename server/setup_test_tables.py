"""
Script to set up the test database tables
Run: python setup_test_tables.py
"""

import pymysql
import os

# Database connection details
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'dev_user',
    'password': 'Team15',
    'database': 'eventmatcher_test',
    'charset': 'utf8mb4'
}

def setup_database():
    """Read and execute the test_schema.sql file to create all tables"""
    
    # Read the SQL file
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'test_schema.sql')
    
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Connect to database
        print(f"Connecting to database: {DB_CONFIG['database']}...")
        connection = pymysql.connect(**DB_CONFIG)
        
        try:
            with connection.cursor() as cursor:
                # Split SQL content by semicolons and execute each statement
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                print(f"Executing {len(statements)} SQL statements...")
                for i, statement in enumerate(statements, 1):
                    if statement:
                        try:
                            cursor.execute(statement)
                            print(f"  [{i}/{len(statements)}] Executed successfully")
                        except Exception as e:
                            print(f"  [{i}/{len(statements)}] Warning: {e}")
                            # Continue even if there's an error (might be DROP TABLE IF EXISTS on non-existent table)
                
                connection.commit()
                print("\n✅ Database setup completed successfully!")
                
                # Verify tables were created
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"\n📋 Created {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                    
        finally:
            connection.close()
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find db.sql file at {sql_file_path}")
        print("Make sure you're running this script from the server directory")
    except pymysql.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    setup_database()
